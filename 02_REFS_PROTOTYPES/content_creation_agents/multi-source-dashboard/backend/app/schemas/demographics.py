from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class DemographicsCreate(BaseModel):
    name: str
    description: Optional[str] = None
    age_range: Dict[str, int] = {}
    gender: List[str] = []
    location: List[str] = []
    interests: List[str] = []
    target_keywords: List[str] = []
    is_public: bool = False

class DemographicsResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_public: bool
    usage_count: int
    success_rate: float
    created_at: datetime
    
    class Config:
        from_attributes = True