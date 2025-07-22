from fastapi import HTTPException, Depends, status
from apps.api.src.auth0.auth import get_current_auth0_user, TokenData

async def get_current_user(current_user_data: TokenData = Depends(get_current_auth0_user)) -> TokenData:
    """
    Retrieves the current authenticated user from Auth0.
    """
    return current_user_data