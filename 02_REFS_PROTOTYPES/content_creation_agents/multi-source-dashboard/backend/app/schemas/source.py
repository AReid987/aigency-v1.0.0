from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.source import SourceType, SourceStatus

class SourceCreate(BaseModel):
    name: str
    display_name: str
    description: Optional[str] = None
    type: SourceType
    base_url: str
    requires_auth: bool = False
    auth_type: Optional[str] = None
    rate_limit_per_minute: int = 60
    config_schema: Dict[str, Any] = {}
    default_config: Dict[str, Any] = {}
    endpoints: Dict[str, Any] = {}

class SourceResponse(BaseModel):
    id: int
    name: str
    display_name: str
    description: Optional[str]
    type: SourceType
    status: SourceStatus
    base_url: str
    requires_auth: bool
    rate_limit_per_minute: int
    created_at: datetime
    last_successful_sync: Optional[datetime]
    error_count: int
    
    class Config:
        from_attributes = True