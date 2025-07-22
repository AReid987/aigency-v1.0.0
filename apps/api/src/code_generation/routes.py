
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from apps.api.src.code_generation.controllers import generate_code

router = APIRouter()

class CodeGenRequest(BaseModel):
    file_path: str
    content: str

@router.post("/code-generation/generate")
def generate(request: CodeGenRequest):
    return generate_code(request.file_path, request.content)
