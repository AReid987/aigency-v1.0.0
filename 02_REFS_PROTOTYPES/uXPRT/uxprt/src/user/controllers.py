import os
from uuid import UUID
from typing import Optional
from supabase import create_client, Client
from gotrue.errors import AuthApiError
from dotenv import load_dotenv

from .models import ProfileCreate, ProfileUpdate, ProfileResponse

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables.")

def create_sync_supabase_client() -> Client:
     """Creates a synchronous Supabase client."""
     return create_client(SUPABASE_URL, SUPABASE_KEY)

async def get_user_profile(user_id: UUID) -> Optional[ProfileResponse]:
    """
    Retrieve a user profile by ID from Supabase.
    """
    supabase = create_sync_supabase_client()
    try:
        response = supabase.table("profiles").select("*").eq("user_id", str(user_id)).single().execute()
        if response.data:
            return ProfileResponse.model_validate(response.data)
        return None
    except Exception as e:
        print(f"Error fetching user profile: {e}")
        return None

async def update_user_profile(user_id: UUID, profile_data: ProfileUpdate) -> Optional[ProfileResponse]:
    """
    Update a user profile by ID in Supabase.
    """
    supabase = create_sync_supabase_client()
    try:
        update_data = profile_data.model_dump(exclude_unset=True) # Only update provided fields
        response = supabase.table("profiles").update(update_data).eq("user_id", str(user_id)).execute()
        if response.data and len(response.data) > 0:
            return ProfileResponse.model_validate(response.data[0])
        return None
    except Exception as e:
        print(f"Error updating user profile: {e}")
        return None

async def create_user_profile(user_id: UUID, profile_data: ProfileCreate) -> Optional[ProfileResponse]:
    """
    Create a new user profile in Supabase.
    This is primarily for manual creation or testing, as the database trigger handles automatic creation on user signup.
    """
    supabase = create_sync_supabase_client()
    try:
        insert_data = profile_data.model_dump()
        insert_data["user_id"] = str(user_id)
        response = supabase.table("profiles").insert(insert_data).execute()
        if response.data and len(response.data) > 0:
            return ProfileResponse.model_validate(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating user profile: {e}")
        return None