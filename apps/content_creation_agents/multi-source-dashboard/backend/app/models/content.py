from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Enum, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class ContentStatus(str, enum.Enum):
    COLLECTED = "collected"
    PROCESSED = "processed"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"
    FAILED = "failed"


class ContentType(str, enum.Enum):
    ARTICLE = "article"
    DISCUSSION = "discussion"
    VIDEO = "video"
    IMAGE = "image"
    LINK = "link"
    COMMENT = "comment"


class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    
    # Content identification
    external_id = Column(String, nullable=True)  # ID from source system
    url = Column(String, nullable=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    
    # Content metadata
    type = Column(Enum(ContentType), default=ContentType.ARTICLE)
    status = Column(Enum(ContentStatus), default=ContentStatus.COLLECTED)
    language = Column(String, default="en")
    
    # Source information
    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship("Source", back_populates="content")
    
    # Run information
    run_id = Column(Integer, ForeignKey("runs.id"))
    run = relationship("Run", back_populates="content")
    
    # Author information
    author = Column(String, nullable=True)
    author_url = Column(String, nullable=True)
    
    # Engagement metrics
    score = Column(Integer, default=0)  # Upvotes, likes, etc.
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    
    # Content analysis
    sentiment_score = Column(Float, nullable=True)  # -1.0 to 1.0
    keywords = Column(JSON, default=list)  # Extracted keywords
    categories = Column(JSON, default=list)  # Content categories
    
    # Timestamps
    published_at = Column(DateTime(timezone=True), nullable=True)  # Original publish time
    collected_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Publishing information
    published_to = Column(JSON, default=list)  # List of platforms published to
    publishing_results = Column(JSON, default=dict)  # Results from each platform
    
    # Additional metadata
    raw_data = Column(JSON, default=dict)  # Original API response
    processing_metadata = Column(JSON, default=dict)  # Processing information