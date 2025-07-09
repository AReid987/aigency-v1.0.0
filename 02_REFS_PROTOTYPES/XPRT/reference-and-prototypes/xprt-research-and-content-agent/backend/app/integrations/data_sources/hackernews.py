from typing import List, Dict, Any
from datetime import datetime
import asyncio
from .base import BaseDataSource

class HackerNewsAPI(BaseDataSource):
    """Hacker News API integration"""
    
    def __init__(self):
        super().__init__(
            name="hackernews",
            base_url="https://hacker-news.firebaseio.com/v0",
            rate_limit=60  # Conservative rate limit
        )
    
    async def fetch_latest_content(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch latest stories from Hacker News"""
        story_type = config.get("story_type", "topstories")
        limit = config.get("limit", 30)
        min_score = config.get("min_score", 0)
        
        # Get story IDs
        story_ids_url = f"{self.base_url}/{story_type}.json"
        story_ids = await self._make_request(story_ids_url)
        
        # Fetch individual stories with concurrency control
        semaphore = asyncio.Semaphore(10)  # Limit concurrent requests
        tasks = []
        
        for story_id in story_ids[:limit]:
            task = self._fetch_story_with_semaphore(semaphore, story_id, min_score)
            tasks.append(task)
        
        stories = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and None values
        valid_stories = [story for story in stories if story and not isinstance(story, Exception)]
        return valid_stories
    
    async def _fetch_story_with_semaphore(self, semaphore: asyncio.Semaphore, story_id: int, min_score: int) -> Dict[str, Any]:
        """Fetch individual story with semaphore control"""
        async with semaphore:
            try:
                story_url = f"{self.base_url}/item/{story_id}.json"
                story_data = await self._make_request(story_url)
                
                # Filter by score and type
                if (story_data.get("score", 0) >= min_score and 
                    story_data.get("type") == "story" and
                    story_data.get("title")):
                    
                    return {
                        "external_id": str(story_data["id"]),
                        "title": story_data["title"],
                        "url": story_data.get("url"),
                        "content": story_data.get("text", ""),
                        "author": story_data.get("by"),
                        "score": story_data.get("score", 0),
                        "comments_count": story_data.get("descendants", 0),
                        "published_at": datetime.fromtimestamp(story_data.get("time", 0)),
                        "type": "article",
                        "raw_data": story_data
                    }
                return None
            except Exception as e:
                print(f"Error fetching story {story_id}: {e}")
                return None
    
    async def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate Hacker News configuration"""
        valid_story_types = ["topstories", "newstories", "beststories", "askstories", "showstories", "jobstories"]
        story_type = config.get("story_type", "topstories")
        
        if story_type not in valid_story_types:
            return False
        
        limit = config.get("limit", 30)
        if not isinstance(limit, int) or limit < 1 or limit > 500:
            return False
        
        min_score = config.get("min_score", 0)
        if not isinstance(min_score, int) or min_score < 0:
            return False
        
        return True
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Return configuration schema for Hacker News"""
        return {
            "type": "object",
            "properties": {
                "story_type": {
                    "type": "string",
                    "enum": ["topstories", "newstories", "beststories", "askstories", "showstories", "jobstories"],
                    "default": "topstories",
                    "description": "Type of stories to fetch"
                },
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 500,
                    "default": 30,
                    "description": "Number of stories to fetch"
                },
                "min_score": {
                    "type": "integer",
                    "minimum": 0,
                    "default": 0,
                    "description": "Minimum score threshold for stories"
                }
            },
            "required": []
        }