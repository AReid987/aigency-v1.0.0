from sqlalchemy import Column, Integer, String, JSON, DateTime, Text, Boolean, Float
from sqlalchemy.sql import func
from app.core.database import Base


class Demographics(Base):
    __tablename__ = "demographics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    # Target demographics
    age_range = Column(JSON, default=dict)  # {"min": 18, "max": 65}
    gender = Column(JSON, default=list)  # ["male", "female", "other"]
    location = Column(JSON, default=list)  # Countries/regions
    interests = Column(JSON, default=list)  # Interest categories
    profession = Column(JSON, default=list)  # Professional backgrounds
    
    # Content preferences
    preferred_content_types = Column(JSON, default=list)
    preferred_sources = Column(JSON, default=list)
    excluded_sources = Column(JSON, default=list)
    
    # Engagement patterns
    peak_activity_hours = Column(JSON, default=list)  # Hours of day (0-23)
    preferred_content_length = Column(String, nullable=True)  # "short", "medium", "long"
    engagement_threshold = Column(Float, default=0.0)  # Minimum engagement score
    
    # Keywords and topics
    target_keywords = Column(JSON, default=list)
    excluded_keywords = Column(JSON, default=list)
    trending_topics = Column(JSON, default=list)
    
    # Social media preferences
    platform_preferences = Column(JSON, default=dict)  # Platform-specific settings
    hashtag_strategy = Column(JSON, default=dict)
    
    # Content filtering rules
    sentiment_preference = Column(String, nullable=True)  # "positive", "negative", "neutral", "any"
    content_freshness = Column(Integer, default=24)  # Hours
    min_engagement_score = Column(Integer, default=0)
    
    # Collaboration settings
    is_public = Column(Boolean, default=False)
    is_template = Column(Boolean, default=False)
    collaborators = Column(JSON, default=list)  # User IDs with access
    
    # Usage statistics
    usage_count = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_used_at = Column(DateTime(timezone=True), nullable=True)