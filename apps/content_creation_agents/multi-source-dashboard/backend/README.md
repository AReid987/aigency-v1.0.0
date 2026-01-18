# Multi-Source Dashboard Backend

A comprehensive FastAPI backend for aggregating content from multiple sources and publishing to various platforms.

## Features

- **Multi-Source Data Collection**: Hacker News, Reddit, and extensible architecture for more sources
- **Content Processing**: Automated sentiment analysis, keyword extraction, and categorization
- **Publishing Automation**: Support for Dev.to, WordPress, Ghost, and other platforms
- **Task Scheduling**: Celery-based background job processing with Redis
- **User Management**: JWT authentication with role-based access control
- **Demographics Targeting**: Collaborative demographic profiling and content filtering
- **RESTful API**: Comprehensive API with automatic documentation

## Tech Stack

- **Backend**: FastAPI with Python 3.12
- **Database**: PostgreSQL with async SQLAlchemy
- **Task Queue**: Celery with Redis
- **Authentication**: JWT with bcrypt password hashing
- **Containerization**: Docker and Docker Compose
- **Database Migrations**: Alembic

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)
- PostgreSQL 15+ (if running locally)
- Redis (if running locally)

### Using Docker (Recommended)

1. **Clone and setup environment**:
```bash
cd backend
cp .env.example .env
# Edit .env with your configuration
```

2. **Start all services**:
```bash
docker-compose up -d
```

3. **Initialize database**:
```bash
docker-compose exec backend python scripts/startup.py
```

4. **Access the application**:
- API Documentation: http://localhost:8000/docs
- Task Monitor (Flower): http://localhost:5555
- Login: admin@dashboard.local / admin123

### Local Development

1. **Setup virtual environment**:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Setup environment**:
```bash
cp .env.example .env
# Edit .env with your local database settings
```

4. **Start database and Redis**:
```bash
# Using Docker for dependencies only
docker run -d --name postgres-dev -e POSTGRES_DB=dashboard_db -e POSTGRES_USER=dashboard_user -e POSTGRES_PASSWORD=dashboard_password -p 5432:5432 postgres:15-alpine
docker run -d --name redis-dev -p 6379:6379 redis:7-alpine
```

5. **Initialize database**:
```bash
python scripts/startup.py
```

6. **Start services**:
```bash
# Terminal 1: FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Celery worker
celery -A app.tasks.celery_app worker --loglevel=info

# Terminal 3: Celery beat scheduler
celery -A app.tasks.celery_app beat --loglevel=info

# Terminal 4: Celery monitor (optional)
celery -A app.tasks.celery_app flower --port=5555
```

## API Usage

### Authentication

1. **Register a new user**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "user", "password": "password123", "full_name": "John Doe"}'
```

2. **Login**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@dashboard.local&password=admin123"
```

### Creating a Run

```bash
curl -X POST "http://localhost:8000/api/v1/runs/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech News Aggregator",
    "description": "Collect tech news from various sources",
    "frequency": "daily",
    "filters": {
      "keywords": ["python", "javascript", "ai"],
      "min_score": 10
    }
  }'
```

### Blog Configuration

```bash
curl -X POST "http://localhost:8000/api/v1/blog-configs/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Dev.to Blog",
    "platform": "dev.to",
    "api_key": "YOUR_DEVTO_API_KEY",
    "auto_publish": false,
    "default_tags": ["python", "webdev"],
    "max_posts_per_day": 3
  }'
```

## Data Sources

### Hacker News
- **Authentication**: None required
- **Rate Limit**: 60 requests/minute (self-imposed)
- **Configuration**:
  - `story_type`: "topstories", "newstories", "beststories"
  - `limit`: Number of stories to fetch (1-100)
  - `min_score`: Minimum score threshold

### Reddit
- **Authentication**: OAuth2 required
- **Rate Limit**: 100 requests/minute
- **Setup**: Configure `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` in .env
- **Configuration**:
  - `subreddits`: List of subreddits to monitor
  - `sort`: "hot", "new", "top", "rising"
  - `limit`: Posts per subreddit (1-100)

## Publishing Platforms

### Dev.to
- **Authentication**: API Key
- **Setup**: Get API key from https://dev.to/settings/account
- **Features**: Auto-publishing, tag management, canonical URLs

### WordPress
- **Authentication**: Username + Application Password
- **Setup**: Create application password in WordPress admin
- **Features**: Auto-publishing, category/tag management

### Ghost (Partial)
- **Authentication**: Admin API Key
- **Status**: Basic implementation (needs completion)

## Environment Variables

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/dashboard_db
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
REDDIT_CLIENT_ID=your-reddit-client-id
REDDIT_CLIENT_SECRET=your-reddit-client-secret
GNEWS_API_KEY=your-gnews-api-key  # Optional
NEWSAPI_KEY=your-newsapi-key      # Optional

# Publishing
DEVTO_API_KEY=your-devto-api-key
WORDPRESS_USERNAME=your-wp-username
WORDPRESS_PASSWORD=your-wp-app-password
WORDPRESS_SITE_URL=https://yoursite.com

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   FastAPI App   │    │   Task Queue    │
│                 │    │                 │    │                 │
│ • Hacker News   │◄──►│ • REST API      │◄──►│ • Celery Worker │
│ • Reddit        │    │ • Authentication│    │ • Celery Beat   │
│ • Future APIs   │    │ • CRUD Ops      │    │ • Redis Broker  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │   PostgreSQL    │
                       │   Database      │
                       │                 │
                       │ • Users         │
                       │ • Runs          │
                       │ • Content       │
                       │ • Sources       │
                       └─────────────────┘
```

## Database Schema

- **Users**: Authentication and user management
- **Sources**: Data source configurations
- **Runs**: Content collection campaigns
- **Content**: Collected and processed content
- **BlogConfigs**: Publishing platform configurations
- **Demographics**: Target audience profiles

## Task Scheduling

- **Data Collection**: Runs every 30 minutes for active sources
- **Content Processing**: Processes new content every 15 minutes
- **Auto Publishing**: Publishes approved content every 20 minutes
- **Cleanup**: Removes old content daily at 2 AM

## Development

### Adding New Data Sources

1. Create a new class inheriting from `BaseDataSource`
2. Implement required methods: `fetch_latest_content`, `validate_config`, `get_config_schema`
3. Add to `DATA_SOURCES` dict in `app/tasks/data_collection.py`
4. Create database migration for new source

### Adding Publishing Platforms

1. Add new platform to `PlatformType` enum
2. Implement publishing function in `app/tasks/publishing.py`
3. Add platform-specific configuration schema

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_api.py
```

## Monitoring

- **Health Check**: GET /health
- **Task Monitoring**: Celery Flower at http://localhost:5555
- **API Documentation**: http://localhost:8000/docs
- **Logs**: Check Docker logs or application logs

## Security

- JWT token authentication
- Password hashing with bcrypt
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy
- API rate limiting (configurable)
- CORS protection

## Production Deployment

1. **Environment Setup**:
   - Use strong secrets for `SECRET_KEY`
   - Configure production database
   - Set up Redis cluster if needed
   - Configure external API keys

2. **Security**:
   - Use HTTPS in production
   - Configure proper CORS origins
   - Set up database backups
   - Monitor API usage and rate limits

3. **Scaling**:
   - Use multiple Celery workers
   - Configure database connection pooling
   - Set up load balancing for API servers
   - Monitor resource usage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details