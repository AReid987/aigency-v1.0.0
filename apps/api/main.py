from fastapi import FastAPI
from apps.api.src.agent.routes import router as agent_router
from apps.api.src.scaffolding.routes import router as scaffolding_router
from apps.api.src.code_generation.routes import router as code_generation_router
from apps.api.src.contact.routes import router as contact_router
from apps.api.src.kanban.routes import router as kanban_router

app = FastAPI(
    title="Aigency API",
    description="API for the Aigency application",
    version="0.1.0",
)

app.include_router(agent_router, prefix="/api")
app.include_router(scaffolding_router, prefix="/api")
app.include_router(code_generation_router, prefix="/api")
app.include_router(contact_router, prefix="/api")
app.include_router(kanban_router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Aigency API is running"}
