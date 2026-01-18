from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.auth.security import get_current_active_user
from app.models.user import User
from app.models.source import Source
from app.schemas.source import SourceCreate, SourceResponse

router = APIRouter()

@router.get("/", response_model=List[SourceResponse])
async def read_sources(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Source).offset(skip).limit(limit))
    sources = result.scalars().all()
    return sources

@router.get("/{source_id}", response_model=SourceResponse)
async def read_source(
    source_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Source).where(Source.id == source_id))
    source = result.scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source

@router.post("/", response_model=SourceResponse)
async def create_source(
    source_data: SourceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    source = Source(**source_data.dict())
    db.add(source)
    await db.commit()
    await db.refresh(source)
    return source