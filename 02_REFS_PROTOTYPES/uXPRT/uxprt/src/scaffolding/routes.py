from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from uuid import UUID
from gotrue.types import User as SupabaseUser

from .controllers import generate_project_scaffolding
from ..auth.controllers import get_current_user

scaffolding_router = APIRouter(
    prefix="/projects/{project_id}/scaffold",
    tags=["scaffolding"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

class ScaffoldingRequest(BaseModel):
    project_name: str

@scaffolding_router.post("/", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def scaffold_project_route(
    project_id: UUID,
    scaffolding_request: ScaffoldingRequest,
    current_user: SupabaseUser = Depends(get_current_user)
):
    """
    Generates the file and folder structure for a project.
    """
    # In a real application, you would verify project_id belongs to current_user
    result = await generate_project_scaffolding(project_id, scaffolding_request.project_name)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["error"])
    return result
