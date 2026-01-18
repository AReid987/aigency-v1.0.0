# Technical Architecture Recommendations

## 1. FastAPI + Next.js Integration Patterns

### Recommended Architecture
```
Frontend (Next.js) ↔ API Gateway ↔ Backend (FastAPI) ↔ Database
                                      ↓
                                 Task Queue (Celery/APScheduler)
                                      ↓
                              External APIs (Data Sources)
```

### Integration Best Practices

#### API Structure
- **Separate Deployments**: Deploy FastAPI and Next.js independently
- **API Gateway**: Use nginx or cloud API gateway for routing
- **CORS Configuration**: Properly configure CORS for cross-origin requests

#### Code Example - FastAPI Setup
```python
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import httpx

app = FastAPI(title="Dashboard API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ArticleCreate(BaseModel):
    title: str
    content: str
    platforms: list[str]

@app.post("/api/articles/publish")
async def publish_article(article: ArticleCreate):
    # Multi-platform publishing logic
    tasks = []
    for platform in article.platforms:
        tasks.append(publish_to_platform(platform, article))
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return {"results": results}

async def publish_to_platform(platform: str, article: ArticleCreate):
    async with httpx.AsyncClient() as client:
        # Platform-specific publishing logic
        pass
```

#### Next.js Integration
```typescript
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function publishArticle(articleData: ArticleData) {
  const response = await fetch(`${API_BASE}/api/articles/publish`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(articleData)
  })
  
  if (!response.ok) {
    throw new Error('Failed to publish article')
  }
  
  return response.json()
}
```

### Deployment Recommendations
- **Containerization**: Use Docker for both applications
- **Orchestration**: Kubernetes or Docker Compose
- **Cloud Platforms**: Vercel (Next.js) + Railway/Render (FastAPI)

## 2. Database Architecture Choice

### PostgreSQL vs MongoDB Analysis

#### PostgreSQL - **Recommended Choice**
```sql
-- Schema example for multi-source dashboard
CREATE TABLE data_sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    api_endpoint VARCHAR(255),
    auth_type VARCHAR(20),
    rate_limit_per_minute INTEGER,
    last_sync TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    source_id INTEGER REFERENCES data_sources(id),
    external_id VARCHAR(100),
    published_at TIMESTAMP,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE publishing_queue (
    id SERIAL PRIMARY KEY,
    article_id INTEGER REFERENCES articles(id),
    platform VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    scheduled_at TIMESTAMP,
    published_at TIMESTAMP,
    error_message TEXT
);
```

#### Advantages of PostgreSQL
- **ACID Compliance**: Reliable transactions for publishing operations
- **JSON Support**: JSONB for flexible metadata storage
- **Complex Queries**: Advanced filtering and aggregation
- **Mature Ecosystem**: Extensive tooling and monitoring

#### MongoDB Alternative
```javascript
// MongoDB schema (if chosen)
{
  _id: ObjectId,
  title: String,
  content: String,
  source: {
    name: String,
    external_id: String,
    synced_at: Date
  },
  publishing: [{
    platform: String,
    status: String,
    scheduled_at: Date,
    published_at: Date
  }],
  metadata: Object,
  created_at: Date
}
```

### Database Choice Recommendation
**PostgreSQL** is recommended because:
- Better for complex relationships between articles, sources, and publishing status
- Superior transaction support for publishing workflows
- Excellent JSON support with JSONB
- Better tooling for monitoring and debugging

## 3. Task Scheduling Architecture

### Celery vs APScheduler Comparison

#### Celery - **Recommended for Production**
```python
# celery_app.py
from celery import Celery
from datetime import timedelta

app = Celery('dashboard')
app.config_from_object('celeryconfig')

@app.task(bind=True, max_retries=3)
def sync_data_source(self, source_id):
    try:
        # Fetch data from external API
        source = get_data_source(source_id)
        data = fetch_external_data(source)
        store_articles(data)
        return f"Synced {len(data)} articles from {source.name}"
    except Exception as exc:
        self.retry(countdown=60, exc=exc)

@app.task
def publish_scheduled_articles():
    # Check for articles scheduled for publishing
    scheduled = get_scheduled_articles()
    for article in scheduled:
        publish_article_task.delay(article.id)

# Periodic tasks
app.conf.beat_schedule = {
    'sync-hackernews': {
        'task': 'sync_data_source',
        'schedule': timedelta(minutes=15),
        'args': (1,)  # Hacker News source ID
    },
    'sync-reddit': {
        'task': 'sync_data_source',
        'schedule': timedelta(minutes=30),
        'args': (2,)  # Reddit source ID
    },
    'publish-scheduled': {
        'task': 'publish_scheduled_articles',
        'schedule': timedelta(minutes=5),
    },
}
```

#### APScheduler - **Simpler Alternative**
```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio

class TaskScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
    
    async def start(self):
        # Schedule data source syncing
        self.scheduler.add_job(
            self.sync_hackernews,
            trigger=IntervalTrigger(minutes=15),
            id='sync_hackernews'
        )
        
        self.scheduler.add_job(
            self.sync_reddit,
            trigger=IntervalTrigger(minutes=30),
            id='sync_reddit'
        )
        
        self.scheduler.start()
    
    async def sync_hackernews(self):
        # Sync logic here
        pass
```

### Recommendation: **Celery**
- Better for distributed systems
- Robust error handling and retries
- Monitoring and management tools
- Horizontal scaling capabilities

## 4. AI/ML Services Integration

### Content Generation Services

#### OpenAI API Integration
```python
import openai
from typing import List

class ContentGenerator:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    async def generate_summary(self, articles: List[dict]) -> str:
        content = "\n".join([f"- {article['title']}" for article in articles])
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a tech news summarizer."},
                {"role": "user", "content": f"Summarize these articles:\n{content}"}
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content

    async def generate_article(self, topic: str, sources: List[dict]) -> str:
        # Generate article based on multiple sources
        pass
```

#### Anthropic Claude Integration
```python
import anthropic

class ClaudeGenerator:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
    
    async def generate_analysis(self, data: dict) -> str:
        response = await self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user", 
                "content": f"Analyze this data: {data}"
            }]
        )
        
        return response.content[0].text
```

### Local LLM Option (Ollama)
```python
import httpx

class LocalLLM:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    async def generate(self, prompt: str, model: str = "llama2") -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            return response.json()["response"]
```

## 5. Complete System Architecture

### System Components
```yaml
# docker-compose.yml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
  
  api:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/dashboard
      - REDIS_URL=redis://redis:6379
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=dashboard
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
  
  celery:
    build: ./backend
    command: celery -A celery_app worker -l info
    depends_on:
      - db
      - redis
  
  celery-beat:
    build: ./backend
    command: celery -A celery_app beat -l info
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

### Performance Considerations
- **Caching**: Redis for API responses and session data
- **Connection Pooling**: Database connection management
- **Rate Limiting**: Implement proper rate limiting for external APIs
- **Monitoring**: Use tools like Sentry, Prometheus, or DataDog

### Security Best Practices
- **API Keys**: Store in environment variables or secure vaults
- **Authentication**: JWT tokens with proper expiration
- **Rate Limiting**: Protect against abuse
- **HTTPS**: All communications over secure connections
- **CORS**: Properly configured cross-origin policies