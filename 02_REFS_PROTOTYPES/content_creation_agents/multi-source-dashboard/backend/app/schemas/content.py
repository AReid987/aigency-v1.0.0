from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.models.content import ContentStatus, ContentType

class ContentCreate(BaseModel):
    title: str
    content: Optional[str] = None
    url: Optional[str] = None
    type: ContentType = ContentType.ARTICLE
    author: Optional[str] = None
    external_id: Optional[str] = None

class ContentResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    url: Optional[str]
    type: ContentType
    status: ContentStatus
    source_id: int
    run_id: Optional[int]
    author: Optional[str]
    score: int
    comments_count: int
    published_at: Optional[datetime]
    collected_at: datetime
    
    class Config:
        from_attributes = True