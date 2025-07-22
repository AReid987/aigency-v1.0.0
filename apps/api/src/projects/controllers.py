from typing import Optional

from apps.api.src.projects.models import ProjectCreate, ProjectResponse

async def create_project(user_id: str, project_data: ProjectCreate) -> Optional[ProjectResponse]:
    """
    Creates a new project in Supabase.
    """
    # Supabase client will be passed via dependency injection in routes
    # For now, we'll simulate the creation
    print(f"Simulating project creation for user {user_id}: {project_data.name}")
    return ProjectResponse(project_id="123e4567-e89b-12d3-a456-426614174000", user_id=user_id, name=project_data.name, description=project_data.description)
