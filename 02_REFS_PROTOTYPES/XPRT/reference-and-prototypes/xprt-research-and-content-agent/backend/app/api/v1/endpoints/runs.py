from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.auth.security import get_current_active_user
from app.models.user import User
from app.models.run import Run
from app.schemas.run import RunCreate, RunResponse, RunUpdate

router = APIRouter()

@router.post("/", response_model=RunResponse)
async def create_run(
    run_data: RunCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    run = Run(**run_data.dict(), owner_id=current_user.id)
    db.add(run)
    await db.commit()
    await db.refresh(run)
    return run

@router.get("/", response_model=List[RunResponse])
async def read_runs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(
        select(Run).where(Run.owner_id == current_user.id).offset(skip).limit(limit)
    )
    runs = result.scalars().all()
    return runs

@router.get("/{run_id}", response_model=RunResponse)
async def read_run(
    run_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Run).where(Run.id == run_id, Run.owner_id == current_user.id))
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run

@router.put("/{run_id}", response_model=RunResponse)
async def update_run(
    run_id: int,
    run_update: RunUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Run).where(Run.id == run_id, Run.owner_id == current_user.id))
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    update_data = run_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(run, field, value)
    
    await db.commit()
    await db.refresh(run)
    return run

@router.delete("/{run_id}")
async def delete_run(
    run_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Run).where(Run.id == run_id, Run.owner_id == current_user.id))
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    await db.delete(run)
    await db.commit()
    return {"message": "Run deleted successfully"}