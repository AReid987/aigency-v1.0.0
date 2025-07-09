from celery import current_task
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import List, Dict, Any

from app.tasks.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models.source import Source
from app.models.content import Content
from app.models.run import Run, RunStatus
from app.integrations.data_sources.hackernews import HackerNewsAPI
from app.integrations.data_sources.reddit import RedditAPI

# Initialize data sources
DATA_SOURCES = {
    "hackernews": HackerNewsAPI(),
    "reddit": RedditAPI(),
}

@celery_app.task(bind=True)
async def collect_from_source(self, source_name: str):
    """Collect content from a specific data source"""
    try:
        current_task.update_state(state="PROGRESS", meta={"status": f"Starting collection from {source_name}"})
        
        async with AsyncSessionLocal() as db:
            # Get source configuration
            result = await db.execute(select(Source).where(Source.name == source_name))
            source = result.scalar_one_or_none()
            
            if not source:
                raise ValueError(f"Source {source_name} not found")
            
            # Get active runs using this source
            active_runs_result = await db.execute(
                select(Run).where(Run.status == RunStatus.ACTIVE)
            )
            active_runs = active_runs_result.scalars().all()
            
            data_source = DATA_SOURCES.get(source_name)
            if not data_source:
                raise ValueError(f"Data source implementation not found for {source_name}")
            
            total_collected = 0
            
            for run in active_runs:
                # Check if this run uses this source
                run_sources = [rs for rs in run.sources if rs.source_id == source.id and rs.is_active]
                if not run_sources:
                    continue
                
                run_source = run_sources[0]
                config = run_source.config or source.default_config
                
                # Collect content
                content_items = await data_source.fetch_latest_content(config)
                
                # Save content to database
                for item_data in content_items:
                    # Check if content already exists
                    existing_result = await db.execute(
                        select(Content).where(
                            Content.external_id == item_data["external_id"],
                            Content.source_id == source.id
                        )
                    )
                    if existing_result.scalar_one_or_none():
                        continue  # Skip duplicate content
                    
                    # Create new content record
                    content = Content(
                        **item_data,
                        source_id=source.id,
                        run_id=run.id
                    )
                    db.add(content)
                    total_collected += 1
                
                # Update run statistics
                run.total_content_collected += len(content_items)
                run.last_run_at = datetime.utcnow()
            
            await db.commit()
            
            # Update source status
            source.last_successful_sync = datetime.utcnow()
            source.error_count = 0
            await db.commit()
            
            return {
                "status": "success",
                "source": source_name,
                "collected": total_collected,
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        # Update source error status
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(Source).where(Source.name == source_name))
            source = result.scalar_one_or_none()
            if source:
                source.error_count += 1
                source.last_error_at = datetime.utcnow()
                source.last_error_message = str(e)
                await db.commit()
        
        current_task.update_state(
            state="FAILURE",
            meta={"error": str(e), "source": source_name}
        )
        raise

@celery_app.task
async def cleanup_old_content():
    """Remove old content based on retention policies"""
    try:
        async with AsyncSessionLocal() as db:
            # Remove content older than 30 days that hasn't been published
            cutoff_date = datetime.utcnow() - timedelta(days=30)
            
            old_content_result = await db.execute(
                select(Content).where(
                    Content.collected_at < cutoff_date,
                    Content.status.in_(["collected", "processed", "rejected"])
                )
            )
            old_content = old_content_result.scalars().all()
            
            for content in old_content:
                await db.delete(content)
            
            await db.commit()
            
            return {
                "status": "success",
                "cleaned_items": len(old_content),
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        raise

@celery_app.task(bind=True)
async def sync_all_active_sources(self):
    """Sync all active data sources"""
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(Source).where(Source.status == "active"))
            active_sources = result.scalars().all()
            
            results = []
            for source in active_sources:
                try:
                    result = await collect_from_source.delay(source.name)
                    results.append({"source": source.name, "status": "queued"})
                except Exception as e:
                    results.append({"source": source.name, "status": "error", "error": str(e)})
            
            return {
                "status": "success",
                "results": results,
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        current_task.update_state(state="FAILURE", meta={"error": str(e)})
        raise