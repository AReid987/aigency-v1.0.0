# src/user/routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from gotrue.types import User as SupabaseUser

from .models import ProfileCreate, ProfileUpdate, ProfileResponse
from .controllers import get_user_profile, update_user_profile, create_user_profile
from ..auth.controllers import get_current_user

profile_router = APIRouter(
    prefix="/profile",
    tags=["profile"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@profile_router.get("/", response_model=ProfileResponse)
async def read_user_profile(current_user: SupabaseUser = Depends(get_current_user)):
    """
    Get the profile of the current authenticated user.
    """
    profile = await get_user_profile(current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile

@profile_router.put("/", response_model=ProfileResponse)
async def update_user_profile_route(
    profile_data: ProfileUpdate,
    current_user: SupabaseUser = Depends(get_current_user)
):
    """
    Update the profile of the current authenticated user.
    """
    updated_profile = await update_user_profile(current_user.id, profile_data)
    if not updated_profile:
        raise HTTPException(status_code=404, detail="User profile not found or update failed")
    return updated_profile

# This endpoint might not be strictly necessary if profiles are auto-created on user signup
# via a database trigger, but it's here for completeness or manual creation if needed.
@profile_router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_user_profile_route(
    profile_data: ProfileCreate,
    current_user: SupabaseUser = Depends(get_current_user)
):
    """
    Create a new user profile for the current authenticated user.
    This is typically handled by a database trigger on user signup.
    """
    # Check if a profile already exists to prevent duplicates if trigger is active
    existing_profile = await get_user_profile(current_user.id)
    if existing_profile:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Profile already exists for this user.")
    
    created_profile = await create_user_profile(current_user.id, profile_data)
    if not created_profile:
        raise HTTPException(status_code=500, detail="Failed to create user profile.")
    return created_profile
