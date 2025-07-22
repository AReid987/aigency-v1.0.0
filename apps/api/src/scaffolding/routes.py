
from fastapi import APIRouter
from apps.api.src.scaffolding.controllers import generate_project_scaffolding
from pydantic import BaseModel
from uuid import UUID

router = APIRouter()

class ProjectScaffoldRequest(BaseModel):
    project_name: str

@router.post("/projects/{project_id}/scaffold")
async def scaffold_project(project_id: UUID, request: ProjectScaffoldRequest):
    return await generate_project_scaffolding(project_id, request.project_name)
