from fastapi import FastAPI, Depends
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL and Key must be set in .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_client():
    yield supabase

from apps.api.src.agent.routes import router as agent_router
from apps.api.src.scaffolding.routes import router as scaffolding_router
from apps.api.src.code_generation.routes import router as code_generation_router
from apps.api.src.contact.routes import router as contact_router
from apps.api.src.kanban.routes import router as kanban_router
from apps.api.src.preview.routes import router as preview_router
from apps.api.src.data_analysis.routes import data_analysis_router
from apps.api.src.auth.routes import api_router as auth_router

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
app.include_router(preview_router, prefix="/api")
app.include_router(data_analysis_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Aigency API is running"}
