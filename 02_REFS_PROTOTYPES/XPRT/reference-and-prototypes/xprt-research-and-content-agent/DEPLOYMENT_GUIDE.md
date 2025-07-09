# Multi-Source Dashboard - Production Deployment Guide

This comprehensive guide covers production deployment of the Multi-Source Dashboard application across different platforms and environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start Deployment](#quick-start-deployment)
3. [Docker Compose Production](#docker-compose-production)
4. [AWS Deployment](#aws-deployment)
5. [Environment Configuration](#environment-configuration)
6. [SSL/TLS Setup](#ssltls-setup)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Backup and Recovery](#backup-and-recovery)
9. [Performance Optimization](#performance-optimization)
10. [Security Best Practices](#security-best-practices)
11. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

**Minimum Production Requirements:**
- **CPU**: 4 cores (8 recommended)
- **Memory**: 8GB RAM (16GB recommended)
- **Storage**: 100GB SSD (500GB recommended)
- **Network**: 1Gbps connection

**Software Requirements:**
- Docker 24.0+ and Docker Compose 2.20+
- Ubuntu 22.04 LTS / CentOS 8+ / Amazon Linux 2
- Nginx 1.20+ (if not using containerized nginx)
- SSL certificate for HTTPS

### Domain and DNS Setup

1. **Domain Configuration**:
   ```bash
   # A records pointing to your server IP
   yourdomain.com     → 1.2.3.4
   www.yourdomain.com → 1.2.3.4
   api.yourdomain.com → 1.2.3.4  # Optional subdomain for API
   ```

2. **Firewall Configuration**:
   ```bash
   # Open required ports
   sudo ufw allow 22    # SSH
   sudo ufw allow 80    # HTTP
   sudo ufw allow 443   # HTTPS
   sudo ufw enable
   ```

## Quick Start Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### 2. Application Deployment

```bash
# Clone repository
git clone https://github.com/yourusername/multi-source-dashboard.git
cd multi-source-dashboard

# Copy and configure environment
cp .env.production.example .env.production
nano .env.production  # Edit with your configuration

# Generate SSL certificates (Let's Encrypt)
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copy SSL certificates
sudo mkdir -p ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem
sudo chown -R $USER:$USER ssl/

# Build and deploy
docker-compose -f docker-compose.production.yml up -d

# Verify deployment
curl http://localhost/health
```

## Docker Compose Production

### Full Production Stack

The production deployment includes:

- **Frontend**: React application served by Nginx
- **Backend**: FastAPI application with Gunicorn
- **Database**: PostgreSQL with optimized configuration
- **Cache**: Redis for sessions and task queue
- **Task Queue**: Celery workers and beat scheduler
- **Monitoring**: Prometheus and Grafana
- **Reverse Proxy**: Nginx with SSL termination

### Service Configuration

```yaml
# Key services in docker-compose.production.yml

services:
  postgres:    # Database with production optimizations
  redis:       # Cache and message broker
  backend:     # FastAPI application
  celery-worker: # Background task processing
  celery-beat: # Scheduled task execution
  flower:      # Task queue monitoring
  nginx:       # Reverse proxy and static files
  prometheus:  # Metrics collection
  grafana:     # Monitoring dashboards
```

### Deployment Commands

```bash
# Start all services
docker-compose -f docker-compose.production.yml up -d

# View logs
docker-compose -f docker-compose.production.yml logs -f

# Scale workers
docker-compose -f docker-compose.production.yml up -d --scale celery-worker=4

# Update application
git pull
docker-compose -f docker-compose.production.yml build
docker-compose -f docker-compose.production.yml up -d

# Backup database
docker-compose -f docker-compose.production.yml exec postgres pg_dump -U dashboard_user dashboard_prod > backup.sql
```

## AWS Deployment

### ECS Deployment with Fargate

1. **Create ECS Cluster**:
   ```bash
   aws ecs create-cluster --cluster-name dashboard-prod
   ```

2. **Set up RDS and ElastiCache**:
   ```bash
   # RDS PostgreSQL
   aws rds create-db-instance \
     --db-instance-identifier dashboard-prod \
     --db-instance-class db.t3.medium \
     --engine postgres \
     --master-username dashboard_user \
     --master-user-password $DB_PASSWORD \
     --allocated-storage 100

   # ElastiCache Redis
   aws elasticache create-cache-cluster \
     --cache-cluster-id dashboard-redis \
     --cache-node-type cache.t3.micro \
     --engine redis
   ```

3. **Deploy using ECS CLI**:
   ```bash
   # Configure ECS CLI
   ecs-cli configure --cluster dashboard-prod --region us-west-2

   # Deploy services
   ecs-cli compose -f docker-compose.aws.yml service up
   ```

### EC2 Deployment

```bash
# Launch EC2 instance (t3.large recommended)
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1d0 \
  --instance-type t3.large \
  --key-name your-key-pair \
  --security-group-ids sg-12345678 \
  --subnet-id subnet-12345678

# Connect and deploy
ssh -i your-key.pem ubuntu@ec2-instance-ip
# Follow Quick Start Deployment steps
```

## Environment Configuration

### Production Environment Variables

Create `.env.production` with these essential variables:

```bash
# Database
POSTGRES_DB=dashboard_prod
POSTGRES_USER=dashboard_user
POSTGRES_PASSWORD=your_secure_password

# Security
SECRET_KEY=your_32_plus_character_secret_key
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# External APIs
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret

# Monitoring
SENTRY_DSN=https://your-sentry-dsn
GRAFANA_PASSWORD=your_grafana_password
```

### Configuration Management

1. **Environment-specific configs**:
   ```
   .env.production     # Production settings
   .env.staging       # Staging settings
   .env.development   # Development settings
   ```

2. **Secrets Management**:
   ```bash
   # Use Docker secrets for sensitive data
   echo "your_secret_password" | docker secret create postgres_password -
   ```

## SSL/TLS Setup

### Let's Encrypt (Recommended)

```bash
# Install certbot
sudo apt install certbot

# Generate certificates
sudo certbot certonly --standalone \
  -d yourdomain.com \
  -d www.yourdomain.com \
  --email your-email@domain.com \
  --agree-tos

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Custom SSL Certificate

```bash
# If you have custom certificates
mkdir -p ssl/
cp your-cert.pem ssl/cert.pem
cp your-private-key.pem ssl/key.pem
chmod 600 ssl/key.pem
```

## Monitoring and Logging

### Prometheus Metrics

Access metrics at: `https://yourdomain.com/metrics`

**Key Metrics**:
- Application response times
- Database connection pool status
- Celery task queue length
- Redis memory usage
- System resource utilization

### Grafana Dashboards

Access Grafana at: `https://yourdomain.com:3000`

**Default Dashboards**:
- Application Performance
- Database Monitoring
- Task Queue Status
- System Resources
- Error Tracking

### Log Management

```bash
# View application logs
docker-compose logs -f backend

# Centralized logging with ELK stack
docker-compose -f docker-compose.logging.yml up -d

# Log rotation configuration
cat > /etc/logrotate.d/dashboard << EOF
/var/log/dashboard/*.log {
    daily
    missingok
    rotate 52
    compress
    notifempty
    create 644 nginx nginx
}
EOF
```

## Backup and Recovery

### Database Backup

```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/database"
mkdir -p $BACKUP_DIR

# Create backup
docker-compose exec postgres pg_dump \
  -U dashboard_user \
  -d dashboard_prod \
  --no-owner --no-acl \
  > "$BACKUP_DIR/backup_$DATE.sql"

# Compress backup
gzip "$BACKUP_DIR/backup_$DATE.sql"

# Upload to S3 (optional)
aws s3 cp "$BACKUP_DIR/backup_$DATE.sql.gz" \
  s3://your-backup-bucket/database/

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete
```

### Full System Backup

```bash
# Backup volumes
docker run --rm \
  -v dashboard_postgres_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/postgres_data_$(date +%Y%m%d).tar.gz -C /data .

# Backup configuration
tar czf config_backup_$(date +%Y%m%d).tar.gz \
  .env.production nginx/ ssl/ monitoring/
```

### Recovery Procedures

```bash
# Database recovery
gunzip < backup_20240101_120000.sql.gz | \
docker-compose exec -T postgres psql \
  -U dashboard_user -d dashboard_prod

# Volume recovery
docker run --rm \
  -v dashboard_postgres_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar xzf /backup/postgres_data_20240101.tar.gz -C /data
```

## Performance Optimization

### Database Optimization

```sql
-- PostgreSQL performance tuning
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
SELECT pg_reload_conf();
```

### Application Optimization

```bash
# Scale services based on load
docker-compose up -d --scale celery-worker=4

# Optimize Redis memory
redis-cli CONFIG SET maxmemory 512mb
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### Nginx Optimization

```nginx
# Add to nginx.conf for better performance
worker_processes auto;
worker_connections 4096;

# Enable HTTP/2
listen 443 ssl http2;

# Optimize SSL
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```

## Security Best Practices

### Application Security

1. **Environment Variables**:
   ```bash
   # Never commit secrets to git
   echo ".env*" >> .gitignore
   ```

2. **Database Security**:
   ```sql
   -- Create read-only user for monitoring
   CREATE USER dashboard_readonly WITH PASSWORD 'readonly_password';
   GRANT CONNECT ON DATABASE dashboard_prod TO dashboard_readonly;
   GRANT USAGE ON SCHEMA public TO dashboard_readonly;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO dashboard_readonly;
   ```

3. **Network Security**:
   ```bash
   # Restrict database access
   iptables -A INPUT -p tcp --dport 5432 -s 172.20.0.0/16 -j ACCEPT
   iptables -A INPUT -p tcp --dport 5432 -j DROP
   ```

### SSL Security

```nginx
# Strong SSL configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers off;

# HSTS
add_header Strict-Transport-Security "max-age=63072000" always;
```

## Troubleshooting

### Common Issues

1. **Service Won't Start**:
   ```bash
   # Check logs
   docker-compose logs service_name
   
   # Check service health
   docker-compose ps
   
   # Restart specific service
   docker-compose restart service_name
   ```

2. **Database Connection Issues**:
   ```bash
   # Test database connection
   docker-compose exec backend python -c "
   from app.core.database import engine
   with engine.connect() as conn:
       result = conn.execute('SELECT 1')
       print('Database connected successfully')
   "
   ```

3. **SSL Certificate Issues**:
   ```bash
   # Check certificate expiry
   openssl x509 -in ssl/cert.pem -text -noout | grep "Not After"
   
   # Test SSL configuration
   curl -I https://yourdomain.com
   ```

4. **High Resource Usage**:
   ```bash
   # Monitor resource usage
   docker stats
   
   # Check application metrics
   curl https://yourdomain.com/metrics
   ```

### Health Checks

```bash
# Application health
curl https://yourdomain.com/health

# Database health
docker-compose exec postgres pg_isready -U dashboard_user

# Redis health
docker-compose exec redis redis-cli ping

# Service status
docker-compose ps
```

### Log Analysis

```bash
# Application errors
docker-compose logs backend | grep ERROR

# Nginx access logs
docker-compose logs nginx | grep "HTTP/1.1\" [45]"

# Database slow queries
docker-compose exec postgres psql -U dashboard_user -d dashboard_prod -c "
SELECT query, mean_exec_time, calls 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;"
```

## Maintenance Procedures

### Regular Maintenance

1. **Weekly Tasks**:
   ```bash
   # Update system packages
   sudo apt update && sudo apt upgrade -y
   
   # Check disk space
   df -h
   
   # Review logs for errors
   docker-compose logs --since 7d | grep ERROR
   ```

2. **Monthly Tasks**:
   ```bash
   # Update Docker images
   docker-compose pull
   docker-compose up -d
   
   # Database maintenance
   docker-compose exec postgres psql -U dashboard_user -d dashboard_prod -c "VACUUM ANALYZE;"
   
   # Clean old Docker images
   docker system prune -f
   ```

3. **SSL Certificate Renewal**:
   ```bash
   # Test renewal
   sudo certbot renew --dry-run
   
   # Renew certificates
   sudo certbot renew
   sudo systemctl reload nginx
   ```

### Scaling Procedures

```bash
# Scale workers horizontally
docker-compose up -d --scale celery-worker=6

# Scale database (vertical)
# 1. Stop application
# 2. Resize database instance
# 3. Update connection limits
# 4. Restart application

# Load balancer setup for multiple instances
# Use nginx upstream or cloud load balancer
```

This deployment guide provides comprehensive instructions for production deployment. Always test deployments in a staging environment before applying to production.