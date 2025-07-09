from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class SourceType(str, enum.Enum):
    NEWS = "news"
    SOCIAL = "social"
    FORUM = "forum"
    BLOG = "blog"
    RSS = "rss"


class SourceStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    RATE_LIMITED = "rate_limited"


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(Enum(SourceType), nullable=False)
    status = Column(Enum(SourceStatus), default=SourceStatus.ACTIVE)
    
    # API Configuration
    base_url = Column(String, nullable=False)
    requires_auth = Column(Boolean, default=False)
    auth_type = Column(String, nullable=True)  # "oauth2", "api_key", "basic"
    
    # Rate limiting
    rate_limit_per_minute = Column(Integer, default=60)
    rate_limit_per_hour = Column(Integer, nullable=True)
    rate_limit_per_day = Column(Integer, nullable=True)
    
    # Configuration schema and defaults
    config_schema = Column(JSON, default=dict)  # JSON schema for validation
    default_config = Column(JSON, default=dict)  # Default configuration
    
    # API endpoints configuration
    endpoints = Column(JSON, default=dict)  # Available endpoints
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_successful_sync = Column(DateTime(timezone=True), nullable=True)
    last_error_at = Column(DateTime(timezone=True), nullable=True)
    
    # Error tracking
    error_count = Column(Integer, default=0)
    last_error_message = Column(Text, nullable=True)
    
    # Relationships
    runs = relationship("RunSource", back_populates="source")
    content = relationship("Content", back_populates="source")