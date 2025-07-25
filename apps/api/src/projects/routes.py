from fastapi import APIRouter, Depends, HTTPException, status

from apps.api.src.auth.controllers import get_current_user
from apps.api.src.auth0.auth import TokenData
from .models import ProjectCreate, ProjectResponse
from .controllers import create_project

project_router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@project_router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project_route(
    project_data: ProjectCreate,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Create a new project for the current authenticated user.
    """
    created_project = await create_project(current_user.sub, project_data)
    if not created_project:
        raise HTTPException(status_code=500, detail="Failed to create project.")
    return created_project
