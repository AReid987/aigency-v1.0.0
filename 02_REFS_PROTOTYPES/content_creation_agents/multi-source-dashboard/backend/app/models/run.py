from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class RunStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class RunFrequency(str, enum.Enum):
    DAILY = "daily"
    TWICE_DAILY = "2x"
    THREE_TIMES_DAILY = "3x"
    FOUR_TIMES_DAILY = "4x"
    HOURLY = "hourly"


class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(RunStatus), default=RunStatus.DRAFT)
    frequency = Column(Enum(RunFrequency), default=RunFrequency.DAILY)
    
    # User relationship
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="runs")
    
    # Configuration
    filters = Column(JSON, default=dict)  # Content filtering rules
    demographics_config = Column(JSON, default=dict)  # Demographics targeting
    publishing_config = Column(JSON, default=dict)  # Publishing settings
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_run_at = Column(DateTime(timezone=True), nullable=True)
    next_run_at = Column(DateTime(timezone=True), nullable=True)
    
    # Statistics
    total_content_collected = Column(Integer, default=0)
    total_content_published = Column(Integer, default=0)
    
    # Relationships
    sources = relationship("RunSource", back_populates="run")
    content = relationship("Content", back_populates="run")


class RunSource(Base):
    """Many-to-many relationship between runs and sources with configuration"""
    __tablename__ = "run_sources"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))
    
    # Source-specific configuration
    is_active = Column(Boolean, default=True)
    config = Column(JSON, default=dict)  # Source-specific settings
    priority = Column(Integer, default=1)  # Collection priority
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    run = relationship("Run", back_populates="sources")
    source = relationship("Source", back_populates="runs")