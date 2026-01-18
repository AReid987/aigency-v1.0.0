"""
Data collection service orchestrator
"""
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.source import Source
from app.models.run import Run, RunStatus
from app.integrations.data_sources.hackernews import HackerNewsAPI
from app.integrations.data_sources.reddit import RedditAPI
from app.utils.logger import get_logger

logger = get_logger(__name__)

class DataCollectionService:
    """Service for orchestrating data collection from multiple sources"""
    
    def __init__(self):
        self.sources = {
            "hackernews": HackerNewsAPI(),
            "reddit": RedditAPI(),
        }
    
    async def get_available_sources(self, db: AsyncSession) -> List[Source]:
        """Get all available and active data sources"""
        result = await db.execute(
            select(Source).where(Source.status == "active")
        )
        return result.scalars().all()
    
    async def get_active_runs(self, db: AsyncSession) -> List[Run]:
        """Get all active runs"""
        result = await db.execute(
            select(Run).where(Run.status == RunStatus.ACTIVE)
        )
        return result.scalars().all()
    
    async def collect_from_source(self, source_name: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Collect content from a specific source"""
        if source_name not in self.sources:
            raise ValueError(f"Unknown source: {source_name}")
        
        source = self.sources[source_name]
        
        # Validate configuration
        if not await source.validate_config(config):
            raise ValueError(f"Invalid configuration for source: {source_name}")
        
        logger.info(f"Collecting content from {source_name}")
        content = await source.fetch_latest_content(config)
        logger.info(f"Collected {len(content)} items from {source_name}")
        
        return content
    
    def get_source_schema(self, source_name: str) -> Dict[str, Any]:
        """Get configuration schema for a source"""
        if source_name not in self.sources:
            raise ValueError(f"Unknown source: {source_name}")
        
        return self.sources[source_name].get_config_schema()
    
    async def validate_source_config(self, source_name: str, config: Dict[str, Any]) -> bool:
        """Validate configuration for a source"""
        if source_name not in self.sources:
            return False
        
        return await self.sources[source_name].validate_config(config)