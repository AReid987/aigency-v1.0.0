from fastapi import APIRouter, Depends
from apps.api.src.auth.controllers import get_current_user
from apps.api.src.auth0.auth import TokenData

api_router = APIRouter()

@api_router.get("/auth/me", response_model=TokenData)
async def read_users_me(current_user: TokenData = Depends(get_current_user)):
    """
    Retrieves information about the current authenticated user from Auth0.
    """
    return current_user