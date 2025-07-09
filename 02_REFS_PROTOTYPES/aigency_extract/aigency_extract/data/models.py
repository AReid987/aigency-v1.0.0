"""Data models for the application."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class ContentType(str, Enum):
    """Type of content being extracted."""

    YOUTUBE = "youtube"
    ARTICLE = "article"
    OTHER = "other"


class Tag(BaseModel):
    """Tag for categorizing content."""

    id: Optional[int] = None
    name: str


class Content(BaseModel):
    """Base model for extracted content."""

    id: Optional[int] = None
    title: str
    url: HttpUrl
    content_type: ContentType
    extracted_at: datetime = Field(default_factory=datetime.now)
    tags: List[str] = []
    
    # Original metadata
    author: Optional[str] = None
    published_date: Optional[datetime] = None
    duration: Optional[int] = None  # in seconds for videos
    
    # Extracted content
    summary: str
    key_insights: List[str] = []
    main_points: List[str] = []
    quotes: List[str] = []
    questions_raised: List[str] = []
    action_items: List[str] = []
    
    # Additional metadata
    extraction_pattern: str
    extraction_quality: Optional[float] = None  # 0-1 score
    notes: Optional[str] = None


class YouTubeContent(Content):
    """YouTube specific content."""
    
    content_type: ContentType = ContentType.YOUTUBE
    video_id: str
    channel_name: Optional[str] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    transcript: Optional[str] = None


class ArticleContent(Content):
    """Article specific content."""
    
    content_type: ContentType = ContentType.ARTICLE
    domain: str
    word_count: Optional[int] = None
    html_content: Optional[str] = None
