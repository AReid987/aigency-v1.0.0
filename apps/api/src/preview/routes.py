
from fastapi import APIRouter
from apps.api.src.preview.controllers import generate_preview
from uuid import UUID

router = APIRouter()

@router.post("/projects/{project_id}/preview")
async def create_preview(project_id: UUID):
    return await generate_preview(project_id)
