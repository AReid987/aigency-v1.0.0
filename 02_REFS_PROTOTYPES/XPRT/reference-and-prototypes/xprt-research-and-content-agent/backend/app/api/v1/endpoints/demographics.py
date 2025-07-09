from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List

from app.core.database import get_db
from app.auth.security import get_current_active_user
from app.models.user import User
from app.models.demographics import Demographics
from app.schemas.demographics import DemographicsCreate, DemographicsResponse

router = APIRouter()

@router.post("/", response_model=DemographicsResponse)
async def create_demographics(
    demographics_data: DemographicsCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    demographics = Demographics(**demographics_data.dict())
    db.add(demographics)
    await db.commit()
    await db.refresh(demographics)
    return demographics

@router.get("/", response_model=List[DemographicsResponse])
async def read_demographics(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Get public demographics and user's own demographics
    result = await db.execute(
        select(Demographics).where(
            or_(Demographics.is_public == True, Demographics.collaborators.contains([current_user.id]))
        ).offset(skip).limit(limit)
    )
    demographics = result.scalars().all()
    return demographics

@router.get("/{demographics_id}", response_model=DemographicsResponse)
async def read_demographics_item(
    demographics_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Demographics).where(Demographics.id == demographics_id))
    demographics = result.scalar_one_or_none()
    if not demographics:
        raise HTTPException(status_code=404, detail="Demographics not found")
    
    # Check access
    if not demographics.is_public and current_user.id not in demographics.collaborators:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return demographics