
from fastapi import APIRouter, Depends
from src.agent.controllers import get_agent_response, Message

router = APIRouter()

@router.post("/agent/respond")
def respond(message: Message):
    return get_agent_response(message)
