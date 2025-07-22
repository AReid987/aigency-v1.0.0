import os
from uuid import UUID
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

from .models import ProjectCreate, ProjectResponse

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables.")

def create_sync_supabase_client() -> Client:
     """Creates a synchronous Supabase client."""
     return create_client(SUPABASE_URL, SUPABASE_KEY)

async def create_project(user_id: UUID, project_data: ProjectCreate) -> Optional[ProjectResponse]:
    """
    Creates a new project in Supabase.
    """
    supabase = create_sync_supabase_client()
    try:
        insert_data = project_data.model_dump()
        insert_data["user_id"] = str(user_id)
        response = supabase.table("projects").insert(insert_data).execute()
        if response.data and len(response.data) > 0:
            return ProjectResponse.model_validate(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating project: {e}")
        return None
