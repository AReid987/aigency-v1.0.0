"""Data models for the application."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl


class ContentType(str, Enum):
    """Type of content being extracted."""

    YOUTUBE = "youtube"
    ARTICLE = "article"
    OTHER = "other"


class LLMProvider(str, Enum):
    """Supported LLM providers."""

    GEMINI = "gemini"
    MISTRAL = "mistral"
    GROQ = "groq"
    TOGETHERAI = "togetherai"
    HUGGINGFACE = "huggingface"
    OPENROUTER = "openrouter"
    VOIDAI = "voidai"
    CEREBRAS = "cerebras"
    GITHUB = "github"
    CLOUDFLARE = "cloudflare"
    CHUTES = "chutes"
    AIGENCY = "aigency"  # Custom AIgency gateway


class Tag(BaseModel):
    """Tag for categorizing content."""

    id: Optional[int] = None
    name: str


class ExtractionPattern(BaseModel):
    """Extraction pattern definition."""

    name: str
    description: str
    prompt_template: str
    example_output: Optional[str] = None
    source: str = "custom"  # fabric, custom, etc.


class StitchStep(BaseModel):
    """A step in a stitch (chain of patterns)."""

    pattern_name: str
    parameters: Dict[str, Union[str, int, float, bool, None]] = Field(default_factory=dict)
    human_in_loop: bool = False
    

class Stitch(BaseModel):
    """A chain of extraction patterns."""

    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    steps: List[StitchStep]
    created_at: datetime = Field(default_factory=datetime.now)


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
    
    # Extraction metadata
    extraction_pattern: str
    extraction_provider: LLMProvider
    extraction_model: str
    extraction_quality: Optional[float] = None  # 0-1 score
    
    # Extracted content
    summary: str
    key_insights: List[str] = []
    main_points: List[str] = []
    quotes: List[str] = []
    questions_raised: List[str] = []
    action_items: List[str] = []
    
    # Additional fields
    raw_extraction: Optional[str] = None
    notes: Optional[str] = None
    
    # Stitch information (if this content was created as part of a stitch)
    stitch_id: Optional[int] = None
    stitch_step: Optional[int] = None


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
