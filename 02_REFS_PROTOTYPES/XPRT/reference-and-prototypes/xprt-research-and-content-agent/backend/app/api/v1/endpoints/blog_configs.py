from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.auth.security import get_current_active_user
from app.models.user import User
from app.models.blog_config import BlogConfig
from app.schemas.blog_config import BlogConfigCreate, BlogConfigResponse

router = APIRouter()

@router.post("/", response_model=BlogConfigResponse)
async def create_blog_config(
    config_data: BlogConfigCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    blog_config = BlogConfig(**config_data.dict(), user_id=current_user.id)
    db.add(blog_config)
    await db.commit()
    await db.refresh(blog_config)
    return blog_config

@router.get("/", response_model=List[BlogConfigResponse])
async def read_blog_configs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(
        select(BlogConfig).where(BlogConfig.user_id == current_user.id).offset(skip).limit(limit)
    )
    configs = result.scalars().all()
    return configs

@router.get("/{config_id}", response_model=BlogConfigResponse)
async def read_blog_config(
    config_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(BlogConfig).where(BlogConfig.id == config_id, BlogConfig.user_id == current_user.id))
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(status_code=404, detail="Blog config not found")
    return config

@router.delete("/{config_id}")
async def delete_blog_config(
    config_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(BlogConfig).where(BlogConfig.id == config_id, BlogConfig.user_id == current_user.id))
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(status_code=404, detail="Blog config not found")
    
    await db.delete(config)
    await db.commit()
    return {"message": "Blog config deleted successfully"}