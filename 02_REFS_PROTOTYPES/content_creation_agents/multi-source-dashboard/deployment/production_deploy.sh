#!/bin/bash

# Multi-Source Dashboard Production Deployment Script
# Builds and deploys both frontend and backend for production use

set -e  # Exit on any error

echo "🚀 Production Deployment for Multi-Source Dashboard"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

# Configuration
DEPLOY_ENV=${1:-"production"}
BUILD_FRONTEND=${BUILD_FRONTEND:-"true"}
BUILD_BACKEND=${BUILD_BACKEND:-"true"}
RUN_TESTS=${RUN_TESTS:-"true"}

# Pre-deployment checks
check_production_requirements() {
    print_info "Checking production deployment requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is required for production deployment"
        exit 1
    fi
    
    # Check environment files
    if [ ! -f "backend/.env" ]; then
        print_error "Backend .env file not found. Copy from .env.example and configure."
        exit 1
    fi
    
    if [ ! -f "frontend/multi-source-dashboard/.env" ]; then
        print_warning "Frontend .env file not found. Using defaults."
        echo "VITE_API_URL=http://localhost:8000" > frontend/multi-source-dashboard/.env
    fi
    
    print_status "Production requirements check passed"
}

# Build frontend for production
build_frontend() {
    if [ "$BUILD_FRONTEND" != "true" ]; then
        print_info "Skipping frontend build"
        return
    fi
    
    print_info "Building frontend for production..."
    
    cd frontend/multi-source-dashboard
    
    # Install dependencies
    if [ ! -d "node_modules" ]; then
        print_info "Installing frontend dependencies..."
        npm ci --only=production
    fi
    
    # Build production bundle
    print_info "Creating production build..."
    npm run build
    
    # Verify build output
    if [ -d "dist" ] && [ -f "dist/index.html" ]; then
        print_status "Frontend build completed successfully"
        
        # Show build info
        BUILD_SIZE=$(du -sh dist/ | cut -f1)
        print_info "Frontend build size: $BUILD_SIZE"
    else
        print_error "Frontend build failed - dist directory not found"
        exit 1
    fi
    
    cd ../..
}

# Build backend Docker images
build_backend() {
    if [ "$BUILD_BACKEND" != "true" ]; then
        print_info "Skipping backend build"
        return
    fi
    
    print_info "Building backend Docker images..."
    
    cd backend
    
    # Build production images
    docker-compose -f docker-compose.yml build --no-cache
    
    # Verify images were built
    if docker images | grep -q "backend"; then
        print_status "Backend Docker images built successfully"
    else
        print_error "Backend Docker build failed"
        exit 1
    fi
    
    cd ..
}

# Run pre-deployment tests
run_deployment_tests() {
    if [ "$RUN_TESTS" != "true" ]; then
        print_info "Skipping deployment tests"
        return
    fi
    
    print_info "Running pre-deployment tests..."
    
    cd backend
    
    # Start services for testing
    docker-compose up -d
    sleep 15
    
    # Run backend tests
    if docker-compose exec -T backend python -m pytest tests/ -v; then
        print_status "Backend tests passed"
    else
        print_warning "Some backend tests failed - check logs"
    fi
    
    # Run integration tests
    cd ../integration-tests
    if python3 test_integration.py; then
        print_status "Integration tests passed"
    else
        print_warning "Some integration tests failed - check configuration"
    fi
    
    # Stop test services
    cd ../backend
    docker-compose down
    cd ..
}

# Deploy to production environment
deploy_production() {
    print_info "Deploying to production environment..."
    
    case "$DEPLOY_ENV" in
        "docker")
            deploy_docker_production
            ;;
        "local")
            deploy_local_production
            ;;
        "staging")
            deploy_staging
            ;;
        *)
            print_error "Unknown deployment environment: $DEPLOY_ENV"
            print_info "Available environments: docker, local, staging"
            exit 1
            ;;
    esac
}

# Docker production deployment
deploy_docker_production() {
    print_info "Deploying with Docker Compose (Production Mode)..."
    
    cd backend
    
    # Create production docker-compose override
    cat > docker-compose.prod.yml << EOF
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    environment:
      - ENVIRONMENT=production
    restart: unless-stopped
    
  celery-worker:
    restart: unless-stopped
    
  celery-beat:
    restart: unless-stopped
    
  postgres:
    restart: unless-stopped
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
      
  redis:
    restart: unless-stopped
    volumes:
      - redis_prod_data:/data

volumes:
  postgres_prod_data:
  redis_prod_data:
EOF
    
    # Deploy with production configuration
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
    
    # Initialize production database
    sleep 20
    docker-compose exec backend python scripts/startup.py
    
    cd ..
    
    print_status "Docker production deployment completed"
}

# Local production deployment
deploy_local_production() {
    print_info "Setting up local production environment..."
    
    # Backend setup
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi
    
    # Activate virtual environment and install dependencies
    source .venv/bin/activate
    pip install -r requirements.txt
    
    # Set production environment
    export ENVIRONMENT=production
    
    # Start production services
    print_info "Starting production backend services..."
    
    # Start PostgreSQL and Redis (assuming they're installed locally)
    # You might need to start these manually or via systemd
    
    # Initialize database
    python scripts/startup.py
    
    # Start backend server
    gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 &
    BACKEND_PID=$!
    
    # Start Celery worker
    celery -A app.tasks.celery_app worker --loglevel=info &
    WORKER_PID=$!
    
    # Start Celery beat
    celery -A app.tasks.celery_app beat --loglevel=info &
    BEAT_PID=$!
    
    cd ..
    
    # Frontend setup
    if [ -d "frontend/multi-source-dashboard/dist" ]; then
        print_info "Starting frontend server..."
        cd frontend/multi-source-dashboard
        npx serve -s dist -l 3000 &
        FRONTEND_PID=$!
        cd ../..
    fi
    
    # Store PIDs for later cleanup
    echo "$BACKEND_PID $WORKER_PID $BEAT_PID $FRONTEND_PID" > .production_pids
    
    print_status "Local production deployment completed"
}

# Staging deployment
deploy_staging() {
    print_info "Deploying to staging environment..."
    
    # Similar to production but with staging configuration
    cd backend
    
    # Use staging environment variables
    export ENVIRONMENT=staging
    
    # Start staging services
    docker-compose -f docker-compose.yml up -d
    
    # Wait and initialize
    sleep 15
    docker-compose exec backend python scripts/startup.py
    
    cd ..
    
    print_status "Staging deployment completed"
}

# Health check after deployment
verify_deployment() {
    print_info "Verifying deployment health..."
    
    # Check backend health
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null; then
            print_status "Backend API is healthy"
            break
        fi
        if [ $i -eq 30 ]; then
            print_error "Backend health check failed"
            return 1
        fi
        sleep 2
    done
    
    # Check database connectivity
    if curl -s http://localhost:8000/api/v1/sources/ > /dev/null; then
        print_status "Database connectivity confirmed"
    else
        print_warning "Database connectivity test failed"
    fi
    
    # Check task queue
    if curl -s http://localhost:5555 > /dev/null; then
        print_status "Task queue (Flower) is accessible"
    else
        print_warning "Task queue monitor not accessible"
    fi
    
    print_status "Deployment verification completed"
}

# Show deployment information
show_deployment_info() {
    echo ""
    echo "🎉 Production Deployment Complete!"
    echo "================================="
    echo ""
    print_info "Service URLs:"
    echo "  🌐 Backend API:     http://localhost:8000"
    echo "  📚 API Docs:        http://localhost:8000/docs"
    echo "  🌸 Task Monitor:    http://localhost:5555"
    
    if [ "$BUILD_FRONTEND" == "true" ]; then
        echo "  🖥️  Frontend:       http://localhost:3000"
    fi
    
    echo ""
    print_info "Deployment Environment: $DEPLOY_ENV"
    echo ""
    print_info "Monitoring Commands:"
    echo "  📊 View logs:       docker-compose -f backend/docker-compose.yml logs -f"
    echo "  📈 Check status:    docker-compose -f backend/docker-compose.yml ps"
    echo "  🔄 Restart:         docker-compose -f backend/docker-compose.yml restart"
    echo "  🛑 Stop:            docker-compose -f backend/docker-compose.yml down"
    echo ""
    print_warning "Remember to:"
    echo "  🔐 Configure SSL/TLS for production"
    echo "  🛡️  Set up firewall rules"
    echo "  📊 Configure monitoring and alerting"
    echo "  💾 Set up database backups"
    echo ""
}

# Cleanup function
cleanup_failed_deployment() {
    print_error "Deployment failed, cleaning up..."
    
    # Stop any running services
    if [ -f "backend/docker-compose.yml" ]; then
        cd backend
        docker-compose down 2>/dev/null || true
        cd ..
    fi
    
    # Kill any background processes
    if [ -f ".production_pids" ]; then
        kill $(cat .production_pids) 2>/dev/null || true
        rm .production_pids
    fi
}

# Signal handlers
trap cleanup_failed_deployment ERR

# Main execution
main() {
    print_info "Starting production deployment process..."
    print_info "Environment: $DEPLOY_ENV"
    print_info "Build Frontend: $BUILD_FRONTEND"
    print_info "Build Backend: $BUILD_BACKEND"
    print_info "Run Tests: $RUN_TESTS"
    echo ""
    
    check_production_requirements
    build_frontend
    build_backend
    run_deployment_tests
    deploy_production
    verify_deployment
    show_deployment_info
    
    print_status "Production deployment completed successfully!"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-frontend)
            BUILD_FRONTEND="false"
            shift
            ;;
        --skip-backend)
            BUILD_BACKEND="false"
            shift
            ;;
        --skip-tests)
            RUN_TESTS="false"
            shift
            ;;
        --help)
            echo "Usage: $0 [environment] [options]"
            echo ""
            echo "Environments:"
            echo "  docker    - Deploy with Docker Compose (default)"
            echo "  local     - Deploy locally with virtual environment"
            echo "  staging   - Deploy to staging environment"
            echo ""
            echo "Options:"
            echo "  --skip-frontend    Skip frontend build"
            echo "  --skip-backend     Skip backend build"
            echo "  --skip-tests       Skip testing phase"
            echo "  --help             Show this help message"
            exit 0
            ;;
        *)
            DEPLOY_ENV="$1"
            shift
            ;;
    esac
done

# Run main function
main