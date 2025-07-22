from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    project_id: UUID
    user_id: UUID
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True