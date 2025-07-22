from fastapi import FastAPI

# Import routers from different modules
from src.agent.routes import router as agent_router # Corrected variable name
from src.auth.routes import api_router as auth_router
from src.user.routes import profile_router as user_router
from src.search.routes import api_router as search_router
from src.data_analysis.routes import data_analysis_router
from src.projects.routes import project_router
from src.messages.routes import message_router
from src.scaffolding.routes import scaffolding_router

app = FastAPI(
    title="uXPRT API",
    description="API for the uXPRT Knowledge OS",
    version="0.1.0",
)

# Include routers
app.include_router(agent_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth")
app.include_router(user_router, prefix="/api/user")
app.include_router(search_router, prefix="/api/search")
app.include_router(data_analysis_router, prefix="/api/data-analysis")
app.include_router(project_router, prefix="/api/projects")
app.include_router(message_router, prefix="/api/projects")
app.include_router(scaffolding_router, prefix="/api/projects")

@app.get("/")
async def read_root():
    return {
    "message": "uXPRT API is running"
}