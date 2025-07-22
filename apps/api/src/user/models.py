from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class ProfileBase(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

class ProfileCreate(ProfileBase):
    # For creation, user_id is typically handled by the backend/trigger
    pass

class ProfileUpdate(ProfileBase):
    # For updates, all fields are optional
    pass

class ProfileResponse(ProfileBase):
    user_id: UUID
    created_at: Optional[str] = None  # Supabase returns ISO format string
    updated_at: Optional[str] = None  # Supabase returns ISO format string

    class Config:
        from_attributes = True  # For Pydantic V2