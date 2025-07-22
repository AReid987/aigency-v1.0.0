
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

class Message(BaseModel):
    text: str

def get_agent_response(message: Message) -> dict:
    """
    Generates a response from the agent.
    """
    # Simple acknowledgement
    return {"text": f"Understood. You said: '{message.text}'. I'm ready to help you build it. Let's start by creating the project structure."}
