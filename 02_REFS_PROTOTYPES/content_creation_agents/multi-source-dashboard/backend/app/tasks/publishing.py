from celery import current_task
from sqlalchemy import select
from datetime import datetime
from typing import Dict, Any, List
import httpx

from app.tasks.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models.content import Content, ContentStatus
from app.models.blog_config import BlogConfig, PlatformType
from app.models.run import Run
from app.core.config import settings

@celery_app.task(bind=True)
async def auto_publish_approved_content(self):
    """Automatically publish approved content to configured platforms"""
    try:
        current_task.update_state(state="PROGRESS", meta={"status": "Publishing content"})
        
        async with AsyncSessionLocal() as db:
            # Get content ready for publishing
            result = await db.execute(
                select(Content).where(Content.status == ContentStatus.APPROVED).limit(20)
            )
            content_to_publish = result.scalars().all()
            
            published_count = 0
            
            for content in content_to_publish:
                try:
                    # Get run configuration
                    run_result = await db.execute(select(Run).where(Run.id == content.run_id))
                    run = run_result.scalar_one_or_none()
                    
                    if not run or not run.publishing_config.get("auto_publish", False):
                        continue
                    
                    # Get blog configurations for the user
                    blog_configs_result = await db.execute(
                        select(BlogConfig).where(
                            BlogConfig.user_id == run.owner_id,
                            BlogConfig.is_active == True,
                            BlogConfig.auto_publish == True
                        )
                    )
                    blog_configs = blog_configs_result.scalars().all()
                    
                    if not blog_configs:
                        continue
                    
                    # Publish to each configured platform
                    for blog_config in blog_configs:
                        result = await publish_to_platform(content, blog_config)
                        if result.get("success"):
                            published_count += 1
                            
                            # Update content status
                            if content.published_to is None:
                                content.published_to = []
                            content.published_to.append(blog_config.platform.value)
                            
                            if content.publishing_results is None:
                                content.publishing_results = {}
                            content.publishing_results[blog_config.platform.value] = result
                    
                    # Mark as published if successful
                    if content.published_to:
                        content.status = ContentStatus.PUBLISHED
                        blog_config.total_published += 1
                        blog_config.last_published_at = datetime.utcnow()
                    
                except Exception as e:
                    print(f"Error publishing content {content.id}: {e}")
                    content.status = ContentStatus.FAILED
                    if content.publishing_results is None:
                        content.publishing_results = {}
                    content.publishing_results["error"] = str(e)
            
            await db.commit()
            
            return {
                "status": "success",
                "published": published_count,
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        current_task.update_state(state="FAILURE", meta={"error": str(e)})
        raise

async def publish_to_platform(content: Content, blog_config: BlogConfig) -> Dict[str, Any]:
    """Publish content to a specific platform"""
    try:
        if blog_config.platform == PlatformType.DEVTO:
            return await publish_to_devto(content, blog_config)
        elif blog_config.platform == PlatformType.WORDPRESS:
            return await publish_to_wordpress(content, blog_config)
        elif blog_config.platform == PlatformType.GHOST:
            return await publish_to_ghost(content, blog_config)
        else:
            return {"success": False, "error": f"Platform {blog_config.platform} not implemented"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

async def publish_to_devto(content: Content, blog_config: BlogConfig) -> Dict[str, Any]:
    """Publish to Dev.to platform"""
    if not blog_config.api_key:
        return {"success": False, "error": "No API key configured"}
    
    # Format content for Dev.to
    article_data = {
        "article": {
            "title": content.title,
            "body_markdown": _format_content_for_devto(content),
            "published": blog_config.auto_publish,
            "tags": blog_config.default_tags[:4],  # Dev.to allows max 4 tags
            "canonical_url": content.url if content.url else None
        }
    }
    
    headers = {
        "api-key": blog_config.api_key,
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://dev.to/api/articles",
            json=article_data,
            headers=headers,
            timeout=30.0
        )
        
        if response.status_code == 201:
            result_data = response.json()
            return {
                "success": True,
                "platform_id": result_data.get("id"),
                "url": result_data.get("url"),
                "published_at": datetime.utcnow().isoformat()
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}"
            }

async def publish_to_wordpress(content: Content, blog_config: BlogConfig) -> Dict[str, Any]:
    """Publish to WordPress via REST API"""
    if not blog_config.username or not blog_config.password:
        return {"success": False, "error": "WordPress credentials not configured"}
    
    post_data = {
        "title": content.title,
        "content": _format_content_for_wordpress(content),
        "status": "publish" if blog_config.auto_publish else "draft",
        "categories": blog_config.default_categories,
        "tags": blog_config.default_tags
    }
    
    api_url = f"{blog_config.site_url}/wp-json/wp/v2/posts"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            api_url,
            json=post_data,
            auth=(blog_config.username, blog_config.password),
            timeout=30.0
        )
        
        if response.status_code == 201:
            result_data = response.json()
            return {
                "success": True,
                "platform_id": result_data.get("id"),
                "url": result_data.get("link"),
                "published_at": datetime.utcnow().isoformat()
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}"
            }

async def publish_to_ghost(content: Content, blog_config: BlogConfig) -> Dict[str, Any]:
    """Publish to Ghost CMS"""
    if not blog_config.api_key:
        return {"success": False, "error": "Ghost API key not configured"}
    
    # Ghost Admin API implementation would go here
    return {"success": False, "error": "Ghost publishing not fully implemented"}

def _format_content_for_devto(content: Content) -> str:
    """Format content for Dev.to markdown"""
    formatted = f"# {content.title}\n\n"
    
    if content.summary:
        formatted += f"{content.summary}\n\n"
    
    if content.content:
        formatted += f"{content.content}\n\n"
    
    # Add source attribution
    if content.url:
        formatted += f"---\n\n*Originally posted at: [{content.url}]({content.url})*\n\n"
    
    if content.author:
        formatted += f"*Author: {content.author}*\n\n"
    
    # Add disclaimer
    formatted += "*This content was automatically curated from various sources.*\n"
    
    return formatted

def _format_content_for_wordpress(content: Content) -> str:
    """Format content for WordPress HTML"""
    formatted = f"<h1>{content.title}</h1>\n\n"
    
    if content.summary:
        formatted += f"<p><strong>{content.summary}</strong></p>\n\n"
    
    if content.content:
        # Simple markdown to HTML conversion
        html_content = content.content.replace('\n', '<br>\n')
        formatted += f"<div>{html_content}</div>\n\n"
    
    # Add source attribution
    if content.url:
        formatted += f"<hr>\n<p><em>Originally posted at: <a href='{content.url}'>{content.url}</a></em></p>\n"
    
    if content.author:
        formatted += f"<p><em>Author: {content.author}</em></p>\n"
    
    return formatted

@celery_app.task(bind=True)
async def publish_single_content(self, content_id: int, blog_config_id: int):
    """Publish a single piece of content to a specific platform"""
    try:
        async with AsyncSessionLocal() as db:
            # Get content and blog config
            content_result = await db.execute(select(Content).where(Content.id == content_id))
            content = content_result.scalar_one_or_none()
            
            blog_config_result = await db.execute(select(BlogConfig).where(BlogConfig.id == blog_config_id))
            blog_config = blog_config_result.scalar_one_or_none()
            
            if not content or not blog_config:
                return {"success": False, "error": "Content or blog config not found"}
            
            # Publish
            result = await publish_to_platform(content, blog_config)
            
            if result.get("success"):
                # Update content
                if content.published_to is None:
                    content.published_to = []
                content.published_to.append(blog_config.platform.value)
                
                if content.publishing_results is None:
                    content.publishing_results = {}
                content.publishing_results[blog_config.platform.value] = result
                
                content.status = ContentStatus.PUBLISHED
                blog_config.total_published += 1
                
                await db.commit()
            
            return result
            
    except Exception as e:
        current_task.update_state(state="FAILURE", meta={"error": str(e)})
        raise