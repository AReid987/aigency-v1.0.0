from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.models.run import RunStatus, RunFrequency

class RunCreate(BaseModel):
    name: str
    description: Optional[str] = None
    frequency: RunFrequency = RunFrequency.DAILY
    filters: Dict[str, Any] = {}
    demographics_config: Dict[str, Any] = {}
    publishing_config: Dict[str, Any] = {}

class RunUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[RunStatus] = None
    frequency: Optional[RunFrequency] = None
    filters: Optional[Dict[str, Any]] = None
    demographics_config: Optional[Dict[str, Any]] = None
    publishing_config: Optional[Dict[str, Any]] = None

class RunResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: RunStatus
    frequency: RunFrequency
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    last_run_at: Optional[datetime]
    next_run_at: Optional[datetime]
    total_content_collected: int
    total_content_published: int
    
    class Config:
        from_attributes = True