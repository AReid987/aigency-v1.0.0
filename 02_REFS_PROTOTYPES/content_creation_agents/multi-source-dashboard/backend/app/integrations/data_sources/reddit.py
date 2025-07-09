from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx
from .base import BaseDataSource
from app.core.config import settings

class RedditAPI(BaseDataSource):
    """Reddit API integration with OAuth2"""
    
    def __init__(self):
        super().__init__(
            name="reddit",
            base_url="https://oauth.reddit.com",
            rate_limit=100  # 100 requests per minute for OAuth
        )
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
    
    async def _get_access_token(self) -> str:
        """Get OAuth2 access token"""
        if (self.access_token and self.token_expires_at and 
            datetime.now() < self.token_expires_at):
            return self.access_token
        
        auth_url = "https://www.reddit.com/api/v1/access_token"
        auth_data = {
            "grant_type": "client_credentials"
        }
        headers = {
            "User-Agent": settings.REDDIT_USER_AGENT
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                auth_url,
                data=auth_data,
                headers=headers,
                auth=(settings.REDDIT_CLIENT_ID, settings.REDDIT_CLIENT_SECRET)
            )
            response.raise_for_status()
            token_data = response.json()
            
            self.access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 3600)
            self.token_expires_at = datetime.now().timestamp() + expires_in
            
            return self.access_token
    
    async def _make_authenticated_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make authenticated request to Reddit API"""
        token = await self._get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": settings.REDDIT_USER_AGENT
        }
        
        url = f"{self.base_url}{endpoint}"
        return await self._make_request(url, params=params, headers=headers)
    
    async def fetch_latest_content(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch latest posts from specified subreddits"""
        subreddits = config.get("subreddits", ["programming"])
        sort_type = config.get("sort", "hot")  # hot, new, top, rising
        limit = config.get("limit", 25)
        min_score = config.get("min_score", 0)
        time_filter = config.get("time_filter", "day")  # hour, day, week, month, year, all
        
        all_posts = []
        
        for subreddit in subreddits:
            try:
                endpoint = f"/r/{subreddit}/{sort_type}"
                params = {
                    "limit": limit,
                    "raw_json": 1
                }
                
                if sort_type == "top":
                    params["t"] = time_filter
                
                response = await self._make_authenticated_request(endpoint, params)
                posts_data = response.get("data", {}).get("children", [])
                
                for post_item in posts_data:
                    post = post_item.get("data", {})
                    
                    # Filter by score and other criteria
                    if (post.get("score", 0) >= min_score and 
                        not post.get("is_self", False) and  # Skip text posts
                        post.get("title")):
                        
                        all_posts.append({
                            "external_id": post["id"],
                            "title": post["title"],
                            "url": post.get("url"),
                            "content": post.get("selftext", ""),
                            "author": post.get("author"),
                            "score": post.get("score", 0),
                            "comments_count": post.get("num_comments", 0),
                            "published_at": datetime.fromtimestamp(post.get("created_utc", 0)),
                            "type": "article",
                            "subreddit": subreddit,
                            "raw_data": post
                        })
                        
            except Exception as e:
                print(f"Error fetching from r/{subreddit}: {e}")
                continue
        
        return all_posts
    
    async def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate Reddit configuration"""
        if not settings.REDDIT_CLIENT_ID or not settings.REDDIT_CLIENT_SECRET:
            return False
        
        subreddits = config.get("subreddits", [])
        if not isinstance(subreddits, list) or not subreddits:
            return False
        
        valid_sorts = ["hot", "new", "top", "rising"]
        sort_type = config.get("sort", "hot")
        if sort_type not in valid_sorts:
            return False
        
        return True
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Return configuration schema for Reddit"""
        return {
            "type": "object",
            "properties": {
                "subreddits": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["programming"],
                    "description": "List of subreddits to monitor"
                },
                "sort": {
                    "type": "string",
                    "enum": ["hot", "new", "top", "rising"],
                    "default": "hot",
                    "description": "Sort order for posts"
                },
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100,
                    "default": 25,
                    "description": "Number of posts to fetch per subreddit"
                },
                "min_score": {
                    "type": "integer",
                    "minimum": 0,
                    "default": 0,
                    "description": "Minimum score threshold"
                },
                "time_filter": {
                    "type": "string",
                    "enum": ["hour", "day", "week", "month", "year", "all"],
                    "default": "day",
                    "description": "Time filter for 'top' sort"
                }
            },
            "required": ["subreddits"]
        }