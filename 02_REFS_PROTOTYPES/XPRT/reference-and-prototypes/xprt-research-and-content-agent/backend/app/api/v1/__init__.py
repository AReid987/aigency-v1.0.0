from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, runs, sources, content, demographics, blog_configs

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(runs.router, prefix="/runs", tags=["runs"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(demographics.router, prefix="/demographics", tags=["demographics"])
api_router.include_router(blog_configs.router, prefix="/blog-configs", tags=["blog-configs"])