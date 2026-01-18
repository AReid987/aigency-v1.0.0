from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.models.blog_config import PlatformType

class BlogConfigCreate(BaseModel):
    name: str
    platform: PlatformType
    site_url: Optional[str] = None
    api_key: Optional[str] = None
    username: Optional[str] = None
    auto_publish: bool = False
    default_tags: List[str] = []
    min_score_threshold: int = 0
    max_posts_per_day: int = 5

class BlogConfigResponse(BaseModel):
    id: int
    name: str
    platform: PlatformType
    is_active: bool
    user_id: int
    auto_publish: bool
    total_published: int
    total_failed: int
    created_at: datetime
    
    class Config:
        from_attributes = True