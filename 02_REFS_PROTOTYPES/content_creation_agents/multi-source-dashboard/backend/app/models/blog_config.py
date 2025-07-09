from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, DateTime, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class PlatformType(str, enum.Enum):
    DEVTO = "dev.to"
    WORDPRESS = "wordpress"
    GHOST = "ghost"
    MEDIUM = "medium"
    HASHNODE = "hashnode"


class BlogConfig(Base):
    __tablename__ = "blog_configs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    platform = Column(Enum(PlatformType), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # User relationship
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="blog_configs")
    
    # Platform configuration
    site_url = Column(String, nullable=True)
    api_endpoint = Column(String, nullable=True)
    
    # Authentication
    api_key = Column(String, nullable=True)  # Encrypted
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)  # Encrypted
    oauth_token = Column(String, nullable=True)  # Encrypted
    
    # Publishing settings
    auto_publish = Column(Boolean, default=False)
    default_tags = Column(JSON, default=list)
    default_categories = Column(JSON, default=list)
    content_template = Column(Text, nullable=True)
    
    # Content formatting
    add_source_attribution = Column(Boolean, default=True)
    add_disclaimer = Column(Boolean, default=True)
    custom_footer = Column(Text, nullable=True)
    
    # Publishing rules
    min_score_threshold = Column(Integer, default=0)
    max_posts_per_day = Column(Integer, default=5)
    exclude_keywords = Column(JSON, default=list)
    include_keywords = Column(JSON, default=list)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_published_at = Column(DateTime(timezone=True), nullable=True)
    
    # Statistics
    total_published = Column(Integer, default=0)
    total_failed = Column(Integer, default=0)
    
    # Platform-specific configuration
    platform_config = Column(JSON, default=dict)