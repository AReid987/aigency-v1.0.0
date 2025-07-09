from fastapi import FastAPI

# Import routers from different modules
from src.agent.routes import router as agent_router # Corrected variable name
from src.auth.routes import api_router as auth_router
from src.user.routes import api_router as user_router
from src.search.routes import api_router as search_router

app = FastAPI(
    title="uXPRT API",
    description="API for the uXPRT Knowledge OS",
    version="0.1.0",
)

# Include routers
app.include_router(agent_router, prefix="/api/agent")
app.include_router(auth_router, prefix="/api/auth")
app.include_router(user_router, prefix="/api/user")
app.include_router(search_router, prefix="/api/search")

@app.get("/")
async def read_root():
    return {
    "message": "uXPRT API is running"
}