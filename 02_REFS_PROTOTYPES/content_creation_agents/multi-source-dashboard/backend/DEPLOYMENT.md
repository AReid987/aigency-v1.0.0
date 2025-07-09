# Deployment Guide

## Quick Start (Docker)

1. **Clone and configure**:
```bash
cd backend
cp .env.example .env
# Edit .env with your configuration
```

2. **Start all services**:
```bash
make start-dev
```

3. **Access**:
- API: http://localhost:8000/docs
- Tasks: http://localhost:5555
- Login: admin@dashboard.local / admin123

## Manual Setup

### Prerequisites
- Python 3.12+
- PostgreSQL 15+
- Redis 7+

### Installation
```bash
# Install dependencies
make install-dev

# Setup database
make setup

# Start services (in separate terminals)
make dev           # FastAPI server
make celery-worker # Background tasks
make celery-beat   # Task scheduler
make celery-flower # Task monitor
```

## Environment Configuration

### Required Variables
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
```

### Optional APIs
```bash
REDDIT_CLIENT_ID=your-reddit-client
REDDIT_CLIENT_SECRET=your-reddit-secret
DEVTO_API_KEY=your-devto-key
```

## Production Deployment

### Docker Production
```bash
make prod-build
make prod-up
```

### Manual Production
1. Set `ENVIRONMENT=production`
2. Use strong `SECRET_KEY`
3. Configure SSL/HTTPS
4. Set up monitoring
5. Configure backups

## Health Checks

- API Health: GET /health
- Database: Check PostgreSQL connection
- Redis: Check task queue status
- Tasks: Monitor Celery Flower

## Monitoring

- **Logs**: Docker logs or application logs
- **Tasks**: Celery Flower at :5555
- **Database**: PostgreSQL monitoring
- **API**: FastAPI built-in metrics

## Scaling

- **API**: Multiple FastAPI instances behind load balancer
- **Tasks**: Multiple Celery workers
- **Database**: Connection pooling, read replicas
- **Cache**: Redis clustering

## Backup Strategy

1. **Database**: Regular PostgreSQL dumps
2. **Configuration**: Backup .env files
3. **Logs**: Log rotation and archival
4. **Code**: Git repository backup

## Troubleshooting

### Common Issues

1. **Database Connection**:
   - Check DATABASE_URL format
   - Verify PostgreSQL is running
   - Check network connectivity

2. **Redis Connection**:
   - Verify Redis is running
   - Check REDIS_URL format
   - Test connection manually

3. **API Authentication**:
   - Verify SECRET_KEY is set
   - Check token expiration
   - Validate user credentials

4. **Task Queue**:
   - Check Celery worker status
   - Verify Redis broker connection
   - Monitor task failures in Flower

### Debug Commands
```bash
# Test database connection
python -c "from app.core.database import engine; print('DB OK')"

# Test Redis connection  
redis-cli ping

# Check API health
curl http://localhost:8000/health

# View logs
docker-compose logs -f backend
docker-compose logs -f celery-worker
```