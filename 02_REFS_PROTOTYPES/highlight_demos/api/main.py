"""
Knowledge OS FastAPI Backend
Main API server with database integration and AI agent endpoints
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
import json
import asyncio
from datetime import datetime
import uuid

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/knowledge_os")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI app
app = FastAPI(
    title="Knowledge OS API",
    description="AI-powered knowledge management and agent interaction system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: str
    profile_image: Optional[str] = None
    role: str = "USER"

class User(BaseModel):
    id: str
    name: str
    email: str
    profile_image: Optional[str]
    role: str
    created_at: datetime
    updated_at: datetime

class KnowledgeBaseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    team_id: Optional[str] = None

class KnowledgeBase(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    owner_id: str
    team_id: Optional[str]

class DocumentCreate(BaseModel):
    title: str
    content: str
    content_type: str = "TEXT"
    knowledge_base_id: str
    metadata: Optional[Dict[str, Any]] = None

class Document(BaseModel):
    id: str
    title: str
    content: str
    content_type: str
    vector_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    knowledge_base_id: str
    metadata: Optional[Dict[str, Any]]

class AgentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    type: str = "ASSISTANT"
    capabilities: List[str]
    config: Dict[str, Any]
    knowledge_base_id: Optional[str] = None

class Agent(BaseModel):
    id: str
    name: str
    description: Optional[str]
    type: str
    capabilities: List[str]
    config: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    owner_id: str
    knowledge_base_id: Optional[str]

class QueryCreate(BaseModel):
    content: str
    agent_id: str
    session_id: Optional[str] = None

class Query(BaseModel):
    id: str
    content: str
    response: str
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    session_id: str
    user_id: str

class SearchRequest(BaseModel):
    query: str
    knowledge_base_id: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=50)
    threshold: float = Field(default=0.7, ge=0.0, le=1.0)

class SearchResult(BaseModel):
    id: str
    content: str
    similarity: float
    document: Dict[str, Any]

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication dependency (simplified)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # In production, validate JWT token here
    # For now, return a mock user
    return {
        "id": "user_123",
        "email": "user@example.com",
        "role": "USER"
    }

# Utility functions
def generate_id():
    return str(uuid.uuid4())

def execute_query(db: Session, query: str, params: Dict[str, Any] = None):
    try:
        if params is None:
            params = {}
        result = db.execute(text(query), params)
        if query.lstrip().upper().startswith(("INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER")):
            db.commit()
        return result
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# User endpoints
@app.post("/api/users", response_model=User)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user_id = generate_id()
    query = """
        INSERT INTO users (id, name, email, profile_image, role, created_at, updated_at)
        VALUES (:id, :name, :email, :profile_image, :role, NOW(), NOW())
        RETURNING *
    """
    params = {
        "id": user_id,
        "name": user_data.name,
        "email": user_data.email,
        "profile_image": user_data.profile_image,
        "role": user_data.role
    }

    result = execute_query(db, query, params)
    row = result.fetchone()

    return User(
        id=row.id,
        name=row.name,
        email=row.email,
        profile_image=row.profile_image,
        role=row.role,
        created_at=row.created_at,
        updated_at=row.updated_at
    )

@app.get("/api/users/{user_id}", response_model=User)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    query = "SELECT * FROM users WHERE id = :user_id"
    result = execute_query(db, query, {"user_id": user_id})
    row = result.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    return User(
        id=row.id,
        name=row.name,
        email=row.email,
        profile_image=row.profile_image,
        role=row.role,
        created_at=row.created_at,
        updated_at=row.updated_at
    )

# Knowledge Base endpoints
@app.post("/api/knowledge-bases", response_model=KnowledgeBase)
async def create_knowledge_base(
    kb_data: KnowledgeBaseCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    kb_id = generate_id()
    query = """
        INSERT INTO knowledge_bases (id, name, description, owner_id, team_id, created_at, updated_at)
        VALUES (:id, :name, :description, :owner_id, :team_id, NOW(), NOW())
        RETURNING *
    """
    params = {
        "id": kb_id,
        "name": kb_data.name,
        "description": kb_data.description,
        "owner_id": current_user["id"],
        "team_id": kb_data.team_id
    }

    result = execute_query(db, query, params)
    row = result.fetchone()

    return KnowledgeBase(
        id=row.id,
        name=row.name,
        description=row.description,
        created_at=row.created_at,
        updated_at=row.updated_at,
        owner_id=row.owner_id,
        team_id=row.team_id
    )

@app.get("/api/knowledge-bases", response_model=List[KnowledgeBase])
async def list_knowledge_bases(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = """
        SELECT * FROM knowledge_bases
        WHERE owner_id = :user_id
        ORDER BY created_at DESC
    """
    result = execute_query(db, query, {"user_id": current_user["id"]})
    rows = result.fetchall()

    return [
        KnowledgeBase(
            id=row.id,
            name=row.name,
            description=row.description,
            created_at=row.created_at,
            updated_at=row.updated_at,
            owner_id=row.owner_id,
            team_id=row.team_id
        )
        for row in rows
    ]

# Document endpoints
@app.post("/api/documents", response_model=Document)
async def create_document(
    doc_data: DocumentCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc_id = generate_id()
    vector_id = f"doc_{doc_id}_{int(datetime.utcnow().timestamp())}"

    query = """
        INSERT INTO documents (id, title, content, content_type, vector_id, knowledge_base_id, metadata, created_at, updated_at)
        VALUES (:id, :title, :content, :content_type, :vector_id, :knowledge_base_id, :metadata, NOW(), NOW())
        RETURNING *
    """
    params = {
        "id": doc_id,
        "title": doc_data.title,
        "content": doc_data.content,
        "content_type": doc_data.content_type,
        "vector_id": vector_id,
        "knowledge_base_id": doc_data.knowledge_base_id,
        "metadata": json.dumps(doc_data.metadata) if doc_data.metadata else None
    }

    result = execute_query(db, query, params)
    row = result.fetchone()

    # TODO: Process document for vector search in background

    return Document(
        id=row.id,
        title=row.title,
        content=row.content,
        content_type=row.content_type,
        vector_id=row.vector_id,
        created_at=row.created_at,
        updated_at=row.updated_at,
        knowledge_base_id=row.knowledge_base_id,
        metadata=json.loads(row.metadata) if row.metadata else None
    )

@app.get("/api/documents", response_model=List[Document])
async def list_documents(
    knowledge_base_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if knowledge_base_id:
        query = """
            SELECT d.* FROM documents d
            JOIN knowledge_bases kb ON d.knowledge_base_id = kb.id
            WHERE d.knowledge_base_id = :kb_id AND kb.owner_id = :user_id
            ORDER BY d.created_at DESC
        """
        params = {"kb_id": knowledge_base_id, "user_id": current_user["id"]}
    else:
        query = """
            SELECT d.* FROM documents d
            JOIN knowledge_bases kb ON d.knowledge_base_id = kb.id
            WHERE kb.owner_id = :user_id
            ORDER BY d.created_at DESC
        """
        params = {"user_id": current_user["id"]}

    result = execute_query(db, query, params)
    rows = result.fetchall()

    return [
        Document(
            id=row.id,
            title=row.title,
            content=row.content,
            content_type=row.content_type,
            vector_id=row.vector_id,
            created_at=row.created_at,
            updated_at=row.updated_at,
            knowledge_base_id=row.knowledge_base_id,
            metadata=json.loads(row.metadata) if row.metadata else None
        )
        for row in rows
    ]

# Agent endpoints
@app.post("/api/agents", response_model=Agent)
async def create_agent(
    agent_data: AgentCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    agent_id = generate_id()
    query = """
        INSERT INTO agents (id, name, description, type, capabilities, config, owner_id, knowledge_base_id, created_at, updated_at)
        VALUES (:id, :name, :description, :type, :capabilities, :config, :owner_id, :knowledge_base_id, NOW(), NOW())
        RETURNING *
    """
    params = {
        "id": agent_id,
        "name": agent_data.name,
        "description": agent_data.description,
        "type": agent_data.type,
        "capabilities": json.dumps(agent_data.capabilities),
        "config": json.dumps(agent_data.config),
        "owner_id": current_user["id"],
        "knowledge_base_id": agent_data.knowledge_base_id
    }

    result = execute_query(db, query, params)
    row = result.fetchone()

    return Agent(
        id=row.id,
        name=row.name,
        description=row.description,
        type=row.type,
        capabilities=json.loads(row.capabilities),
        config=json.loads(row.config),
        created_at=row.created_at,
        updated_at=row.updated_at,
        owner_id=row.owner_id,
        knowledge_base_id=row.knowledge_base_id
    )

@app.get("/api/agents", response_model=List[Agent])
async def list_agents(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = """
        SELECT * FROM agents
        WHERE owner_id = :user_id
        ORDER BY created_at DESC
    """
    result = execute_query(db, query, {"user_id": current_user["id"]})
    rows = result.fetchall()

    return [
        Agent(
            id=row.id,
            name=row.name,
            description=row.description,
            type=row.type,
            capabilities=json.loads(row.capabilities),
            config=json.loads(row.config),
            created_at=row.created_at,
            updated_at=row.updated_at,
            owner_id=row.owner_id,
            knowledge_base_id=row.knowledge_base_id
        )
        for row in rows
    ]

# Search endpoints
@app.post("/api/search", response_model=List[SearchResult])
async def semantic_search(
    search_request: SearchRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Placeholder for semantic search
    # In production, this would use the vector search implementation
    base_query = """
        SELECT c.id, c.content, 0.8 as similarity,
               json_build_object('id', d.id, 'title', d.title, 'knowledgeBaseId', d.knowledge_base_id) as document
        FROM chunks c
        JOIN documents d ON c.document_id = d.id
        JOIN knowledge_bases kb ON d.knowledge_base_id = kb.id
    """

    base_query += """
        WHERE kb.owner_id = :user_id
          AND c.content ILIKE :search_query
    """

    if search_request.knowledge_base_id is not None:
        base_query += " AND d.knowledge_base_id = :kb_id"

    base_query += """
        ORDER BY similarity DESC
        LIMIT :limit
    """

    params = {
        "user_id": current_user["id"],
        "search_query": f"%{search_request.query}%",
        "limit": search_request.limit
    }

    query = base_query
    result = execute_query(db, query, params)
    rows = result.fetchall()

    return [
        SearchResult(
            id=row.id,
            content=row.content,
            similarity=row.similarity,
            document=row.document
        )
        for row in rows
    ]

# Query/Chat endpoints
@app.post("/api/query", response_model=Query)
async def process_query(
    query_data: QueryCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create or get session
    session_id = query_data.session_id
    if not session_id:
        session_id = generate_id()
        session_query = """
            INSERT INTO sessions (id, user_id, agent_id, created_at, updated_at)
            VALUES (:id, :user_id, :agent_id, NOW(), NOW())
        """
        execute_query(db, session_query, {
            "id": session_id,
            "user_id": current_user["id"],
            "agent_id": query_data.agent_id
        })

    # Process the query (placeholder - integrate with AI service)
    response = f"This is a response to: {query_data.content}"

    # Store the query and response
    query_id = generate_id()
    store_query = """
        INSERT INTO queries (id, content, response, session_id, user_id, created_at)
        VALUES (:id, :content, :response, :session_id, :user_id, NOW())
        RETURNING *
    """
    result = execute_query(db, store_query, {
        "id": query_id,
        "content": query_data.content,
        "response": response,
        "session_id": session_id,
        "user_id": current_user["id"]
    })
    row = result.fetchone()

    return Query(
        id=row.id,
        content=row.content,
        response=row.response,
        metadata=json.loads(row.metadata) if row.metadata else None,
        created_at=row.created_at,
        session_id=row.session_id,
        user_id=row.user_id
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
