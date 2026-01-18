# Multi-Source Dashboard - System Architecture Documentation

## Overview

The Multi-Source Dashboard is a modern, scalable content aggregation and publishing platform built with microservices architecture principles. This document provides comprehensive technical architecture information for developers, system administrators, and technical stakeholders.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Technology Stack](#technology-stack)
3. [Database Design](#database-design)
4. [API Architecture](#api-architecture)
5. [Data Flow](#data-flow)
6. [Security Architecture](#security-architecture)
7. [Scalability Design](#scalability-design)
8. [Performance Optimization](#performance-optimization)
9. [Monitoring and Observability](#monitoring-and-observability)
10. [Deployment Architecture](#deployment-architecture)

## System Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Load Balancer │    │   External APIs │
│   (React/Vite)  │◄──►│   (Nginx)       │◄──►│   (HN, Reddit)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Gateway   │    │   Backend API   │    │   Task Queue    │
│   (Nginx)       │◄──►│   (FastAPI)     │◄──►│   (Celery)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cache Layer   │    │   Database      │    │   Message Broker│
│   (Redis)       │    │   (PostgreSQL)  │    │   (Redis)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Component Architecture

#### Frontend Layer
- **Technology**: React 18 + TypeScript + Vite
- **State Management**: Zustand + React Query
- **UI Framework**: Tailwind CSS + shadcn/ui
- **Routing**: React Router v6
- **Build Tool**: Vite with optimized production builds

#### Backend Layer
- **API Framework**: FastAPI with async/await
- **Authentication**: JWT with RS256 algorithm
- **ORM**: SQLAlchemy 2.0 with async support
- **Validation**: Pydantic v2 models
- **Documentation**: Auto-generated OpenAPI/Swagger

#### Data Processing Layer
- **Task Queue**: Celery with Redis broker
- **Scheduling**: Celery Beat for periodic tasks
- **Data Sources**: Pluggable integrations (HackerNews, Reddit)
- **Content Processing**: Async pipelines with parallel processing

#### Storage Layer
- **Primary Database**: PostgreSQL 15+ with JSONB support
- **Cache**: Redis 7+ for sessions and temporary data
- **File Storage**: Local filesystem or S3-compatible storage
- **Search**: PostgreSQL full-text search with trigram support

## Technology Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Frontend** | React | 18+ | User interface |
| **Build Tool** | Vite | 4+ | Frontend build system |
| **Backend** | FastAPI | 0.104+ | REST API framework |
| **Database** | PostgreSQL | 15+ | Primary data storage |
| **Cache** | Redis | 7+ | Caching and message broker |
| **Task Queue** | Celery | 5+ | Background job processing |
| **Web Server** | Nginx | 1.25+ | Reverse proxy and static files |
| **Container** | Docker | 24+ | Application containerization |

### Development Dependencies

```python
# Backend Dependencies
fastapi[all]==0.104.1          # Web framework
sqlalchemy[asyncio]==2.0.23    # Database ORM
alembic==1.12.1                # Database migrations
pydantic[email]==2.5.0         # Data validation
celery[redis]==5.3.4           # Task queue
redis==5.0.1                   # Cache and broker
httpx==0.25.2                  # HTTP client
python-jose[cryptography]==3.3.0  # JWT handling
passlib[bcrypt]==1.7.4         # Password hashing
python-multipart==0.0.6        # Form data handling
```

```typescript
// Frontend Dependencies
"react": "^18.2.0"              // UI framework
"react-router-dom": "^6.20.0"   // Routing
"@tanstack/react-query": "^5.8.0"  // Server state
"zustand": "^4.4.7"             // Client state
"axios": "^1.6.0"               // HTTP client
"tailwindcss": "^3.3.6"         // CSS framework
"typescript": "^5.2.2"          // Type checking
"vite": "^5.0.0"                // Build tool
```

### Infrastructure Dependencies

```yaml
# Docker Compose Services
postgresql:15-alpine    # Database
redis:7-alpine         # Cache/Broker
nginx:1.25-alpine      # Web server
node:20-alpine         # Frontend build
python:3.12-slim       # Backend runtime
```

## Database Design

### Entity Relationship Diagram

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Users    │    │    Runs     │    │   Sources   │
│             │    │             │    │             │
│ id (PK)     │◄──►│ id (PK)     │    │ id (PK)     │
│ email       │    │ user_id(FK) │◄──►│ name        │
│ username    │    │ name        │    │ type        │
│ password    │    │ status      │    │ config      │
│ created_at  │    │ frequency   │    │ is_active   │
└─────────────┘    │ filters     │    └─────────────┘
                   │ config      │
                   └─────────────┘
                          │
                          ▼
                   ┌─────────────┐    ┌─────────────┐
                   │   Content   │    │ BlogConfigs │
                   │             │    │             │
                   │ id (PK)     │    │ id (PK)     │
                   │ run_id (FK) │    │ user_id(FK) │
                   │ title       │◄──►│ name        │
                   │ content     │    │ platform    │
                   │ url         │    │ settings    │
                   │ status      │    │ is_active   │
                   │ metadata    │    │ created_at  │
                   └─────────────┘    └─────────────┘
```

### Core Tables

#### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    bio TEXT,
    avatar_url VARCHAR(500)
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_active ON users(is_active);
```

#### Sources Table
```sql
CREATE TABLE sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(200) NOT NULL,
    description TEXT,
    source_type VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    requires_auth BOOLEAN DEFAULT false,
    rate_limits JSONB DEFAULT '{}',
    configuration_schema JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_sources_active ON sources(is_active);
CREATE INDEX idx_sources_type ON sources(source_type);
```

#### Runs Table
```sql
CREATE TABLE runs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'draft',
    frequency VARCHAR(50) NOT NULL,
    filters JSONB DEFAULT '{}',
    demographics_config JSONB DEFAULT '{}',
    publishing_config JSONB DEFAULT '{}',
    last_run TIMESTAMP WITH TIME ZONE,
    next_run TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    error_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0
);

-- Indexes
CREATE INDEX idx_runs_user ON runs(user_id);
CREATE INDEX idx_runs_status ON runs(status);
CREATE INDEX idx_runs_next_run ON runs(next_run);
CREATE INDEX idx_runs_user_status ON runs(user_id, status);
```

#### Content Table
```sql
CREATE TABLE content (
    id SERIAL PRIMARY KEY,
    run_id INTEGER REFERENCES runs(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    content TEXT,
    url VARCHAR(1000),
    author VARCHAR(255),
    source VARCHAR(100) NOT NULL,
    source_id VARCHAR(255),
    score INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    content_type VARCHAR(50) DEFAULT 'article',
    status VARCHAR(50) DEFAULT 'pending_review',
    sentiment VARCHAR(20),
    tags TEXT[],
    metadata JSONB DEFAULT '{}',
    collected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_content_run ON content(run_id);
CREATE INDEX idx_content_status ON content(status);
CREATE INDEX idx_content_source ON content(source);
CREATE INDEX idx_content_collected_at ON content(collected_at);
CREATE INDEX idx_content_score ON content(score);
CREATE INDEX idx_content_tags ON content USING GIN(tags);
CREATE INDEX idx_content_metadata ON content USING GIN(metadata);

-- Full-text search
CREATE INDEX idx_content_search ON content USING GIN(
    to_tsvector('english', title || ' ' || COALESCE(content, ''))
);
```

#### Blog Configurations Table
```sql
CREATE TABLE blog_configs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    platform VARCHAR(50) NOT NULL,
    settings JSONB NOT NULL DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    success_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0
);

-- Indexes
CREATE INDEX idx_blog_configs_user ON blog_configs(user_id);
CREATE INDEX idx_blog_configs_platform ON blog_configs(platform);
CREATE INDEX idx_blog_configs_active ON blog_configs(is_active);
```

#### Run Sources Junction Table
```sql
CREATE TABLE run_sources (
    id SERIAL PRIMARY KEY,
    run_id INTEGER REFERENCES runs(id) ON DELETE CASCADE,
    source_id INTEGER REFERENCES sources(id) ON DELETE CASCADE,
    configuration JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(run_id, source_id)
);

-- Indexes
CREATE INDEX idx_run_sources_run ON run_sources(run_id);
CREATE INDEX idx_run_sources_source ON run_sources(source_id);
```

### Database Optimization

#### Performance Indexes
```sql
-- Composite indexes for common queries
CREATE INDEX idx_content_user_status ON content(run_id, status);
CREATE INDEX idx_content_source_date ON content(source, collected_at DESC);
CREATE INDEX idx_runs_user_active ON runs(user_id, status) WHERE status = 'active';

-- Partial indexes for common filters
CREATE INDEX idx_content_pending ON content(collected_at DESC) 
    WHERE status = 'pending_review';
CREATE INDEX idx_content_approved ON content(collected_at DESC) 
    WHERE status = 'approved';
```

#### Query Optimization
```sql
-- Enable query plan analysis
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM content 
WHERE run_id = 1 AND status = 'pending_review' 
ORDER BY collected_at DESC 
LIMIT 20;

-- Performance monitoring
SELECT schemaname, tablename, attname, n_distinct, correlation 
FROM pg_stats 
WHERE tablename IN ('content', 'runs', 'users');
```

## API Architecture

### RESTful Design Principles

The API follows REST architectural constraints with additional considerations for modern web applications:

#### Resource-Oriented URLs
```
/api/v1/users/{id}              # User resources
/api/v1/runs/{id}               # Run resources
/api/v1/runs/{id}/content       # Nested content resources
/api/v1/content/{id}/approve    # Resource actions
/api/v1/sources/{id}/test       # Resource operations
```

#### HTTP Methods and Status Codes
```
GET    /api/v1/runs         # 200 OK - List resources
POST   /api/v1/runs         # 201 Created - Create resource
GET    /api/v1/runs/{id}    # 200 OK - Get resource
PUT    /api/v1/runs/{id}    # 200 OK - Update resource
DELETE /api/v1/runs/{id}    # 204 No Content - Delete resource
PATCH  /api/v1/runs/{id}    # 200 OK - Partial update

# Error responses
400 Bad Request             # Invalid request data
401 Unauthorized           # Authentication required
403 Forbidden              # Insufficient permissions
404 Not Found              # Resource doesn't exist
422 Unprocessable Entity   # Validation errors
429 Too Many Requests      # Rate limited
500 Internal Server Error  # Server errors
```

### API Versioning Strategy

#### URL Versioning
- **Current Version**: `/api/v1/`
- **Future Versions**: `/api/v2/`, `/api/v3/`
- **Deprecation Policy**: 12 months notice for breaking changes
- **Backward Compatibility**: Non-breaking changes within major versions

#### Version Header Support
```http
# Optional version specification
Accept: application/json; version=1
API-Version: 1
```

### Request/Response Patterns

#### Standard Request Format
```json
{
  "data": {
    "type": "runs",
    "attributes": {
      "name": "Daily Tech News",
      "frequency": "daily"
    },
    "relationships": {
      "sources": {
        "data": [
          {"type": "sources", "id": "1"}
        ]
      }
    }
  }
}
```

#### Standard Response Format
```json
{
  "data": {
    "type": "runs",
    "id": "123",
    "attributes": {
      "name": "Daily Tech News",
      "status": "active",
      "created_at": "2024-01-01T12:00:00Z"
    },
    "relationships": {
      "user": {
        "data": {"type": "users", "id": "456"}
      }
    }
  },
  "meta": {
    "version": "1.0",
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

#### Error Response Format
```json
{
  "errors": [
    {
      "id": "error_123",
      "status": "400",
      "code": "VALIDATION_ERROR",
      "title": "Validation Failed",
      "detail": "The 'frequency' field is required",
      "source": {
        "pointer": "/data/attributes/frequency"
      }
    }
  ],
  "meta": {
    "request_id": "req_456",
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

### Authentication & Authorization

#### JWT Token Structure
```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_123",
    "email": "user@example.com",
    "iat": 1640995200,
    "exp": 1640998800,
    "aud": "multi-source-dashboard",
    "iss": "https://yourdomain.com",
    "permissions": ["read:content", "write:runs"]
  }
}
```

#### Permission System
```python
# Role-based permissions
PERMISSIONS = {
    "user": [
        "read:own_content",
        "write:own_runs",
        "manage:own_blog_configs"
    ],
    "admin": [
        "read:all_content",
        "write:all_runs",
        "manage:system"
    ]
}
```

## Data Flow

### Content Collection Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Trigger   │───►│  Collection │───►│ Processing  │
│   (Celery   │    │   Tasks     │    │   Pipeline  │
│    Beat)    │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
                           │                   │
                           ▼                   ▼
                   ┌─────────────┐    ┌─────────────┐
                   │  External   │    │  Content    │
                   │    APIs     │    │ Enhancement │
                   │(HN, Reddit) │    │(Tags, etc.) │
                   └─────────────┘    └─────────────┘
                           │                   │
                           ▼                   ▼
                   ┌─────────────┐    ┌─────────────┐
                   │   Data      │    │  Database   │
                   │ Validation  │───►│   Storage   │
                   │             │    │             │
                   └─────────────┘    └─────────────┘
```

### Detailed Data Flow Steps

#### 1. Collection Trigger
```python
# Celery Beat scheduler
@celery.task
def schedule_collections():
    """Run every minute to check for due collections"""
    due_runs = get_due_runs()
    for run in due_runs:
        collect_content_for_run.delay(run.id)
```

#### 2. Content Collection
```python
@celery.task(bind=True, max_retries=3)
def collect_content_for_run(self, run_id):
    """Collect content from configured sources"""
    try:
        run = get_run(run_id)
        
        # Parallel collection from multiple sources
        collection_tasks = []
        for source_config in run.sources:
            task = collect_from_source.delay(
                source_config.source_id,
                source_config.configuration,
                run.filters
            )
            collection_tasks.append(task)
        
        # Wait for all collections to complete
        results = [task.get() for task in collection_tasks]
        
        # Aggregate and process results
        content_items = aggregate_results(results)
        
        # Process each content item
        for item in content_items:
            process_content_item.delay(item, run_id)
            
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
```

#### 3. Content Processing Pipeline
```python
@celery.task
def process_content_item(content_data, run_id):
    """Process individual content item"""
    
    # 1. Duplicate detection
    if is_duplicate(content_data):
        return
    
    # 2. Content filtering
    if not passes_filters(content_data, run_id):
        return
    
    # 3. Content enhancement
    enhanced_content = enhance_content(content_data)
    
    # 4. Sentiment analysis
    sentiment = analyze_sentiment(enhanced_content['content'])
    
    # 5. Tag generation
    tags = generate_tags(enhanced_content)
    
    # 6. Save to database
    content_item = save_content(
        enhanced_content,
        sentiment=sentiment,
        tags=tags,
        run_id=run_id
    )
    
    # 7. Trigger notifications if needed
    if content_item.score > HIGH_SCORE_THRESHOLD:
        notify_high_quality_content.delay(content_item.id)
```

### Publishing Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Content   │───►│  Approval   │───►│ Publishing  │
│   Review    │    │   Queue     │    │   Tasks     │
└─────────────┘    └─────────────┘    └─────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Manual/    │    │ Scheduling  │    │ Platform    │
│  Auto       │    │   Engine    │    │ Adapters    │
│ Approval    │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
                           │                   │
                           ▼                   ▼
                   ┌─────────────┐    ┌─────────────┐
                   │   Queue     │    │  External   │
                   │ Management  │    │ Publishing  │
                   │             │    │ Platforms   │
                   └─────────────┘    └─────────────┘
```

## Security Architecture

### Authentication Security

#### Password Security
```python
# Password hashing with bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Increased rounds for security
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

#### JWT Security
```python
# JWT configuration
JWT_ALGORITHM = "RS256"  # RSA-256 for better security
JWT_PRIVATE_KEY = load_private_key()
JWT_PUBLIC_KEY = load_public_key()
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Token validation
def validate_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            JWT_PUBLIC_KEY,
            algorithms=[JWT_ALGORITHM],
            audience="multi-source-dashboard"
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
```

### API Security

#### Rate Limiting
```python
# Redis-based rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"
)

# Apply rate limits
@app.post("/api/v1/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, ...):
    pass

@app.get("/api/v1/content/")
@limiter.limit("100/minute")
async def get_content(request: Request, ...):
    pass
```

#### Input Validation
```python
# Pydantic models for validation
class CreateRunRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    frequency: Literal["daily", "2x", "3x", "4x", "hourly"]
    
    # Custom validation
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
```

#### SQL Injection Prevention
```python
# Using SQLAlchemy ORM prevents SQL injection
async def get_content_by_run(run_id: int, user_id: int):
    query = (
        select(Content)
        .where(Content.run_id == run_id)
        .join(Run)
        .where(Run.user_id == user_id)
    )
    result = await session.execute(query)
    return result.scalars().all()
```

### Data Security

#### Encryption at Rest
```python
# Database encryption (PostgreSQL)
# Enable TDE (Transparent Data Encryption)
# Configure encrypted storage volumes

# Application-level encryption for sensitive data
from cryptography.fernet import Fernet

class EncryptedField:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def encrypt(self, value: str) -> str:
        return self.cipher.encrypt(value.encode()).decode()
    
    def decrypt(self, encrypted_value: str) -> str:
        return self.cipher.decrypt(encrypted_value.encode()).decode()
```

#### API Key Management
```python
# Secure API key storage
class APIKeyManager:
    def __init__(self):
        self.encryption_key = os.getenv("ENCRYPTION_KEY")
        self.cipher = Fernet(self.encryption_key)
    
    def store_api_key(self, user_id: int, platform: str, api_key: str):
        encrypted_key = self.cipher.encrypt(api_key.encode())
        # Store encrypted key in database
        
    def retrieve_api_key(self, user_id: int, platform: str) -> str:
        encrypted_key = get_encrypted_key(user_id, platform)
        return self.cipher.decrypt(encrypted_key).decode()
```

### Network Security

#### HTTPS Configuration
```nginx
# Nginx SSL configuration
server {
    listen 443 ssl http2;
    
    # SSL certificates
    ssl_certificate /etc/ssl/certs/domain.crt;
    ssl_certificate_key /etc/ssl/private/domain.key;
    
    # SSL security settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=63072000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
}
```

#### CORS Configuration
```python
# FastAPI CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## Scalability Design

### Horizontal Scaling

#### Application Scaling
```yaml
# Docker Compose scaling
services:
  backend:
    scale: 3  # Multiple backend instances
    
  celery-worker:
    scale: 4  # Multiple worker instances
    
  nginx:
    # Load balancer configuration
    upstream backend {
      server backend_1:8000;
      server backend_2:8000;
      server backend_3:8000;
    }
```

#### Database Scaling
```sql
-- Read replicas for scaling reads
CREATE SUBSCRIPTION content_replica
CONNECTION 'host=replica-host dbname=dashboard'
PUBLICATION content_publication;

-- Partitioning for large tables
CREATE TABLE content_2024_01 PARTITION OF content
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

### Vertical Scaling

#### Resource Optimization
```yaml
# Docker resource limits
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

#### Database Optimization
```sql
-- PostgreSQL configuration for performance
shared_buffers = 25% of RAM
effective_cache_size = 75% of RAM
maintenance_work_mem = 256MB
wal_buffers = 16MB
checkpoint_completion_target = 0.9
```

### Caching Strategy

#### Multi-Level Caching
```python
# Application-level caching
from functools import lru_cache
import redis

# Memory cache for frequently accessed data
@lru_cache(maxsize=1000)
def get_source_config(source_id: int):
    return fetch_source_config(source_id)

# Redis cache for session data
redis_client = redis.Redis(host='redis', port=6379, db=0)

def cache_user_session(user_id: int, session_data: dict):
    redis_client.setex(
        f"session:{user_id}",
        3600,  # 1 hour expiry
        json.dumps(session_data)
    )
```

#### Database Query Caching
```sql
-- Query result caching
SELECT pg_stat_statements_reset();

-- Monitor slow queries
SELECT query, mean_exec_time, calls, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Load Balancing

#### Application Load Balancing
```nginx
# Nginx upstream configuration
upstream backend_api {
    least_conn;  # Load balancing method
    server backend1:8000 max_fails=3 fail_timeout=30s;
    server backend2:8000 max_fails=3 fail_timeout=30s;
    server backend3:8000 max_fails=3 fail_timeout=30s;
}

# Health checks
location /health {
    proxy_pass http://backend_api;
    proxy_connect_timeout 2s;
    proxy_read_timeout 2s;
}
```

#### Database Connection Pooling
```python
# SQLAlchemy connection pooling
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,           # Base pool size
    max_overflow=30,        # Additional connections
    pool_pre_ping=True,     # Validate connections
    pool_recycle=3600,      # Recycle connections hourly
)
```

## Performance Optimization

### Database Performance

#### Query Optimization
```sql
-- Analyze query performance
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT c.*, r.name as run_name
FROM content c
JOIN runs r ON c.run_id = r.id
WHERE r.user_id = 123
  AND c.status = 'pending_review'
ORDER BY c.collected_at DESC
LIMIT 20;

-- Optimized query with proper indexes
CREATE INDEX CONCURRENTLY idx_content_user_status_date
ON content (run_id, status, collected_at DESC)
WHERE status = 'pending_review';
```

#### Database Maintenance
```sql
-- Regular maintenance tasks
VACUUM ANALYZE content;
REINDEX INDEX CONCURRENTLY idx_content_search;

-- Automated maintenance
SELECT cron.schedule('vacuum-content', '0 2 * * *', 'VACUUM ANALYZE content;');
```

### Application Performance

#### Async Processing
```python
# Asynchronous database operations
async def get_content_batch(run_id: int, limit: int = 100):
    async with AsyncSession(engine) as session:
        query = (
            select(Content)
            .where(Content.run_id == run_id)
            .limit(limit)
        )
        result = await session.execute(query)
        return result.scalars().all()

# Concurrent processing
async def process_multiple_runs(run_ids: List[int]):
    tasks = [collect_content_for_run(run_id) for run_id in run_ids]
    await asyncio.gather(*tasks)
```

#### Memory Optimization
```python
# Streaming large datasets
def stream_content(query):
    """Stream large result sets to avoid memory issues"""
    with Session(engine) as session:
        result = session.execute(query)
        while True:
            batch = result.fetchmany(1000)
            if not batch:
                break
            yield batch
```

### Frontend Performance

#### Bundle Optimization
```typescript
// Code splitting with React.lazy
const DashboardPage = lazy(() => import('./pages/DashboardPage'));
const ContentPage = lazy(() => import('./pages/ContentPage'));

// Route-based code splitting
const router = createBrowserRouter([
  {
    path: "/dashboard",
    element: <Suspense fallback={<Loading />}><DashboardPage /></Suspense>
  }
]);
```

#### API Optimization
```typescript
// React Query for caching and background updates
const useContent = (runId: number) => {
  return useQuery({
    queryKey: ['content', runId],
    queryFn: () => api.getContent({ run_id: runId }),
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
  });
};
```

## Monitoring and Observability

### Application Monitoring

#### Health Checks
```python
@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    
    checks = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": app.version,
        "checks": {}
    }
    
    # Database health
    try:
        async with AsyncSession(engine) as session:
            await session.execute(text("SELECT 1"))
        checks["checks"]["database"] = "healthy"
    except Exception as e:
        checks["checks"]["database"] = f"unhealthy: {str(e)}"
        checks["status"] = "unhealthy"
    
    # Redis health
    try:
        await redis_client.ping()
        checks["checks"]["redis"] = "healthy"
    except Exception as e:
        checks["checks"]["redis"] = f"unhealthy: {str(e)}"
        checks["status"] = "unhealthy"
    
    # External API health
    for source in ["hackernews", "reddit"]:
        try:
            status = await check_external_api_health(source)
            checks["checks"][f"api_{source}"] = status
        except Exception as e:
            checks["checks"][f"api_{source}"] = f"unhealthy: {str(e)}"
    
    return checks
```

#### Metrics Collection
```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
active_connections = Gauge('active_database_connections', 'Active database connections')

# Middleware for metrics collection
@app.middleware("http")
async def add_prometheus_metrics(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    # Record metrics
    request_count.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()
    
    request_duration.observe(time.time() - start_time)
    
    return response
```

### Logging Strategy

#### Structured Logging
```python
import structlog
import logging

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Usage in application
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    
    logger.info(
        "request_started",
        method=request.method,
        path=request.url.path,
        user_agent=request.headers.get("user-agent")
    )
    
    response = await call_next(request)
    
    logger.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration=time.time() - start_time
    )
    
    return response
```

### Error Tracking

#### Sentry Integration
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[
        FastApiIntegration(auto_enabling_integrations=True),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=0.1,  # 10% of transactions
    profiles_sample_rate=0.1,
    environment="production"
)
```

## Deployment Architecture

### Container Architecture

#### Multi-Stage Docker Builds
```dockerfile
# Backend Dockerfile
FROM python:3.12-slim as base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base as development
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]

FROM base as production
COPY . .
RUN useradd --create-home --shell /bin/bash app
USER app
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker"]
```

#### Frontend Build
```dockerfile
# Frontend Dockerfile
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine as production
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Infrastructure as Code

#### Docker Compose Production
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  backend:
    build:
      context: ./backend
      target: production
    environment:
      DATABASE_URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres/${POSTGRES_DB}
      REDIS_URL: redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started

volumes:
  postgres_data:
  redis_data:
```

### Cloud Deployment

#### AWS Architecture
```
Internet Gateway
     │
     ▼
Application Load Balancer
     │
     ▼
┌─────────────────────────────────────────┐
│              VPC                        │
│                                         │
│  ┌─────────────┐    ┌─────────────┐    │
│  │   Public    │    │   Private   │    │
│  │   Subnet    │    │   Subnet    │    │
│  │             │    │             │    │
│  │  ┌───────┐  │    │  ┌───────┐  │    │
│  │  │  ECS  │  │    │  │  RDS  │  │    │
│  │  │Service│  │    │  │Postgres│    │
│  │  └───────┘  │    │  └───────┘  │    │
│  │             │    │             │    │
│  │  ┌───────┐  │    │  ┌───────┐  │    │
│  │  │ Auto  │  │    │  │ElastiC│  │    │
│  │  │Scaling│  │    │  │ Cache │  │    │
│  │  │ Group │  │    │  │ Redis │  │    │
│  │  └───────┘  │    │  └───────┘  │    │
│  └─────────────┘    └─────────────┘    │
└─────────────────────────────────────────┘
```

#### Kubernetes Deployment
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dashboard-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: dashboard-backend
  template:
    metadata:
      labels:
        app: dashboard-backend
    spec:
      containers:
      - name: backend
        image: dashboard-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

This architecture documentation provides a comprehensive technical overview of the Multi-Source Dashboard system. It serves as a reference for developers, system administrators, and technical stakeholders involved in maintaining, scaling, or extending the platform.