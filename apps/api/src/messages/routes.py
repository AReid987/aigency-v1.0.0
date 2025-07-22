from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from uuid import UUID

from apps.api.src.auth.controllers import get_current_user
from apps.api.src.auth0.auth import TokenData
from .controllers import handle_message

message_router = APIRouter(
    prefix="/projects/{project_id}/messages",
    tags=["messages"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

class MessageRequest(BaseModel):
    message: str

@message_router.post("/")
async def post_message(
    project_id: UUID,
    message_request: MessageRequest,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Handles incoming messages for a specific project.
    """
    # In a real application, you would store the message in the database
    # and trigger a more complex AI response generation process.
    ai_response = await handle_message(project_id, message_request.message)
    return ai_response
