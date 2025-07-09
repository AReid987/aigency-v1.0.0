from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid # For UserResponse model

# Import the new controller functions and dependencies
from .controllers import (
    register_user as ctrl_register_user,
    login_user as ctrl_login_user,
    logout_user as ctrl_logout_user,
    get_current_user # Removed get_supabase_client import
)
from supabase import Client # Corrected Client import
from gotrue.types import User as SupabaseUser # For typing the user object

api_router = APIRouter()

# --- Request Models ---
class UserRegisterRequest(BaseModel):
    username: Optional[str] = None # Supabase uses email as primary identifier, username can be metadata
    email: EmailStr
    password: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

# --- Response Models ---
class UserRegistrationResponse(BaseModel):
    message: str
    user_id: uuid.UUID
    email: EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: uuid.UUID

class UserResponse(BaseModel):
    id: uuid.UUID
    email: Optional[EmailStr] = None
    # Add other user fields you expect from Supabase user object if needed
    # For example: created_at, updated_at, etc.
    # We'll keep it simple for now.

class MessageResponse(BaseModel):
    message: str

# Changed route to be synchronous
@api_router.post('/register', response_model=UserRegistrationResponse, status_code=status.HTTP_201_CREATED)
def register_route(user_data: UserRegisterRequest): # Removed supabase dependency
    """
    Register a new user.
    The username is optional and will be stored in user_metadata if provided.
    """
    try:
        # Controller function is now sync and creates its own client
        response_data = ctrl_register_user( # Removed await
            email=user_data.email,
            password=user_data.password,
            username=user_data.username # Pass username to controller
            # Removed supabase=supabase argument
        )
        return UserRegistrationResponse(**response_data)
    except HTTPException as e:
        raise e # Re-raise HTTPException from controller
    except Exception as e:
        # Catch-all for unexpected errors during registration
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Registration failed: {str(e)}")


# Changed route to be synchronous
@api_router.post('/login', response_model=TokenResponse)
def login_route(user_data: UserLoginRequest): # Removed supabase dependency
    """
    Log in a user and return an access token.
    """
    try:
        # Controller function is now sync and creates its own client
        response_data = ctrl_login_user( # Removed await
            email=user_data.email,
            password=user_data.password
            # Removed supabase=supabase argument
        )
        return TokenResponse(**response_data)
    except HTTPException as e:
        raise e # Re-raise HTTPException from controller
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Login failed: {str(e)}")


# Changed route to be synchronous
@api_router.post('/logout', response_model=MessageResponse)
def logout_route(
    # The logout_user controller uses Depends(oauth2_scheme) internally now
    # We just need to call it. FastAPI handles injecting the dependency to the controller.
    # We no longer need to inject supabase_client here as controller creates its own.
    logout_response: dict = Depends(ctrl_logout_user) # Call controller via Depends
):
    """
    Log out the current user by invalidating their session token.
    The dependency injection handles passing the token to the controller.
    """
    # The result from the dependency is directly returned
    try:
        return MessageResponse(**logout_response)
    except Exception as e: # Catch potential pydantic validation errors etc.
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Logout response processing failed: {str(e)}")


# Changed route to sync as get_current_user dependency is now sync
@api_router.get('/users/me', response_model=UserResponse)
def read_users_me(current_user: SupabaseUser = Depends(get_current_user)): # get_current_user is sync
    """
    Get current authenticated user's details.
    This is an example of a protected route.
    """
    # The SupabaseUser object might have more fields; adjust UserResponse model as needed.
    return UserResponse(id=current_user.id, email=current_user.email)

# Example of how you might add more protected routes:
# @api_router.get("/some-protected-resource")
# async def get_protected_resource(current_user: SupabaseUser = Depends(get_current_user)):
#     return {"message": f"Hello user {current_user.id}, you can access this."}