
from fastapi import APIRouter
from apps.api.src.kanban.controllers import get_kanban_board_data, update_story_status
from uuid import UUID
from pydantic import BaseModel

router = APIRouter()

class UpdateStoryStatusRequest(BaseModel):
    new_status: str

@router.get("/projects/{project_id}/board")
async def get_board(project_id: UUID):
    return await get_kanban_board_data(project_id)

@router.patch("/stories/{story_id}/status")
async def update_status(story_id: str, request: UpdateStoryStatusRequest):
    return await update_story_status(story_id, request.new_status)
