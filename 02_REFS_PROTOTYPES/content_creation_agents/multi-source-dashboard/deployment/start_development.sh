#!/bin/bash

# Multi-Source Dashboard Development Environment Startup Script
# This script starts all services required for development

set -e  # Exit on any error

echo "🚀 Starting Multi-Source Dashboard Development Environment"
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if required tools are installed
check_requirements() {
    print_info "Checking requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check Node.js (for frontend development)
    if ! command -v node &> /dev/null; then
        print_warning "Node.js is not installed. Frontend development will not be available."
    fi
    
    # Check Python (for backend development)
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 is not installed. Backend development will not be available."
    fi
    
    print_status "Requirements check completed"
}

# Start backend services with Docker
start_backend_services() {
    print_info "Starting backend services (PostgreSQL, Redis, FastAPI, Celery)..."
    
    cd backend
    
    # Copy environment file if it doesn't exist
    if [ ! -f .env ]; then
        print_warning ".env file not found, copying from .env.example"
        cp .env.example .env
        print_warning "Please edit .env file with your configuration"
    fi
    
    # Start services with Docker Compose
    docker-compose up -d
    
    # Wait for services to be ready
    print_info "Waiting for services to start..."
    sleep 10
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_status "Backend services started successfully"
    else
        print_error "Some backend services failed to start"
        docker-compose logs
        exit 1
    fi
    
    # Initialize database
    print_info "Initializing database..."
    docker-compose exec backend python scripts/startup.py
    
    cd ..
}

# Start frontend development server
start_frontend() {
    print_info "Starting frontend development server..."
    
    cd frontend/multi-source-dashboard
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_info "Installing frontend dependencies..."
        npm install
    fi
    
    # Copy environment file if it doesn't exist
    if [ ! -f .env ]; then
        print_warning ".env file not found, creating with default values"
        echo "VITE_API_URL=http://localhost:8000" > .env
    fi
    
    # Start development server in background
    print_info "Starting Vite development server..."
    npm run dev &
    FRONTEND_PID=$!
    
    cd ../..
    
    print_status "Frontend development server started (PID: $FRONTEND_PID)"
}

# Wait for services to be fully ready
wait_for_services() {
    print_info "Waiting for all services to be ready..."
    
    # Wait for backend API
    print_info "Checking backend API health..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null; then
            print_status "Backend API is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            print_error "Backend API failed to start within timeout"
            exit 1
        fi
        sleep 2
    done
    
    # Wait for frontend
    print_info "Checking frontend server..."
    for i in {1..20}; do
        if curl -s http://localhost:5173 > /dev/null; then
            print_status "Frontend server is ready"
            break
        fi
        if [ $i -eq 20 ]; then
            print_warning "Frontend server not responding, but continuing..."
            break
        fi
        sleep 2
    done
}

# Run integration tests
run_integration_tests() {
    print_info "Running integration tests..."
    
    # Check if integration tests directory exists
    if [ -d "integration-tests" ]; then
        cd integration-tests
        
        # Install test dependencies
        pip3 install httpx pytest > /dev/null 2>&1 || print_warning "Could not install test dependencies"
        
        # Run backend integration tests
        if python3 test_integration.py; then
            print_status "Backend integration tests passed"
        else
            print_warning "Some backend integration tests failed"
        fi
        
        cd ..
    else
        print_warning "Integration tests directory not found, skipping tests"
    fi
}

# Display service information
show_service_info() {
    echo ""
    echo "🎉 Development Environment Ready!"
    echo "================================="
    echo ""
    print_info "Service URLs:"
    echo "  🌐 Frontend:        http://localhost:5173"
    echo "  🔧 Backend API:     http://localhost:8000"
    echo "  📚 API Docs:        http://localhost:8000/docs"
    echo "  🌸 Flower (Tasks): http://localhost:5555"
    echo "  🗄️  PostgreSQL:     localhost:5432"
    echo "  🔴 Redis:           localhost:6379"
    echo ""
    print_info "Default Login:"
    echo "  📧 Email:     admin@dashboard.local"
    echo "  🔐 Password:  admin123"
    echo ""
    print_info "Useful Commands:"
    echo "  📊 View logs:       docker-compose -f backend/docker-compose.yml logs -f"
    echo "  🛑 Stop services:   docker-compose -f backend/docker-compose.yml down"
    echo "  🔄 Restart:         ./deployment/restart_development.sh"
    echo "  🧪 Run tests:       python3 integration-tests/test_integration.py"
    echo ""
}

# Cleanup function for graceful shutdown
cleanup() {
    echo ""
    print_info "Shutting down development environment..."
    
    # Stop frontend if running
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    # Stop Docker services
    cd backend
    docker-compose down
    cd ..
    
    print_status "Development environment stopped"
}

# Set up signal handlers for graceful shutdown
trap cleanup EXIT INT TERM

# Main execution
main() {
    check_requirements
    start_backend_services
    start_frontend
    wait_for_services
    run_integration_tests
    show_service_info
    
    # Keep script running
    print_info "Press Ctrl+C to stop all services"
    while true; do
        sleep 1
    done
}

# Run main function
main