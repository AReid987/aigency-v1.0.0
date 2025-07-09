from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional

from app.core.database import get_db
from app.auth.security import get_current_active_user
from app.models.user import User
from app.models.content import Content
from app.models.run import Run
from app.schemas.content import ContentResponse

router = APIRouter()

@router.get("/", response_model=List[ContentResponse])
async def read_content(
    skip: int = 0,
    limit: int = 100,
    run_id: Optional[int] = Query(None),
    source_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Content)
    
    if run_id:
        # Verify user owns the run
        run_result = await db.execute(select(Run).where(Run.id == run_id, Run.owner_id == current_user.id))
        if not run_result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Run not found")
        query = query.where(Content.run_id == run_id)
    
    if source_id:
        query = query.where(Content.source_id == source_id)
    
    result = await db.execute(query.offset(skip).limit(limit))
    content = result.scalars().all()
    return content

@router.get("/{content_id}", response_model=ContentResponse)
async def read_content_item(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Verify user has access to this content
    if content.run_id:
        run_result = await db.execute(select(Run).where(Run.id == content.run_id, Run.owner_id == current_user.id))
        if not run_result.scalar_one_or_none():
            raise HTTPException(status_code=403, detail="Access denied")
    
    return content