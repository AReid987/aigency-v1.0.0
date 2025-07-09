from fastapi import APIRouter
from .controllers import router as search_router

# Create an API router for the search module
api_router = APIRouter()

# Include the search router from the controllers
api_router.include_router(search_router)