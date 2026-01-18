# Multi-Source Dashboard - Integration Testing Guide

This guide provides comprehensive instructions for testing the complete Multi-Source Dashboard application, including frontend-backend integration, data sources, publishing workflows, and end-to-end user journeys.

## Quick Start

### 1. Automated Test Suite (Recommended)

Run all tests with a single command:

```bash
# Start services and run all tests
cd deployment
./run_all_tests.sh

# Or with custom configuration
./run_all_tests.sh --backend-url http://localhost:8000 --frontend-url http://localhost:5173
```

### 2. Docker-Based Testing

For isolated testing environment:

```bash
# Start complete test environment
cd deployment
docker-compose -f docker-test-environment.yml up -d

# Run tests in containers
docker-compose -f docker-test-environment.yml run test-runner

# Cleanup
docker-compose -f docker-test-environment.yml down -v
```

## Test Categories

### 1. Backend API Integration Tests

**Location**: `integration-tests/test_integration.py`

**Tests Include**:
- Backend health check and connectivity
- CORS configuration validation
- User registration and authentication
- Protected endpoint access
- Data source endpoints
- Run management operations
- Content management workflows
- Blog configuration endpoints
- Database connectivity validation
- Error handling scenarios

**Run Manually**:
```bash
cd integration-tests
python3 test_integration.py
```

**Expected Results**:
- ✅ Backend health check passes
- ✅ User registration and login successful
- ✅ All API endpoints accessible
- ✅ Database operations working
- ✅ Error handling properly implemented

### 2. Data Source Integration Tests

**Location**: `deployment/test_data_sources.py`

**Tests Include**:
- Hacker News API direct access
- Reddit API connectivity and rate limiting
- Content filtering and categorization
- Scheduling system validation
- Error recovery mechanisms

**Run Manually**:
```bash
cd deployment
python3 test_data_sources.py
```

**Expected Results**:
- ✅ External APIs accessible
- ✅ Content collection working
- ✅ Rate limiting compliance
- ✅ Filtering logic functional

### 3. Publishing Integration Tests

**Location**: `deployment/test_publishing.py`

**Tests Include**:
- WordPress, Ghost, and Dev.to API connectivity
- Content formatting for different platforms
- Authentication methods validation
- Publishing workflow simulation
- Rate limiting compliance
- Error recovery testing

**Run Manually**:
```bash
cd deployment
python3 test_publishing.py
```

**Expected Results**:
- ✅ Publishing platform APIs accessible
- ✅ Content formatting working
- ✅ Authentication flows valid
- ✅ Workflow logic functional

### 4. Frontend-Backend Integration Tests

**Location**: `integration-tests/test_frontend_backend.py`

**Tests Include**:
- Frontend accessibility and loading
- Login/registration form functionality
- API connectivity from frontend
- Navigation and routing
- Responsive design validation
- Error handling in UI

**Requirements**:
- Chrome or Chromium browser
- ChromeDriver installed
- Frontend server running

**Run Manually**:
```bash
# Install Selenium if not installed
pip install selenium

cd integration-tests
python3 test_frontend_backend.py
```

**Expected Results**:
- ✅ Frontend loads successfully
- ✅ Forms functional
- ✅ API calls working from browser
- ✅ Navigation working
- ✅ Responsive design functional

### 5. End-to-End Workflow Tests

**Location**: `deployment/test_e2e_workflow.py`

**Tests Include**:
- Complete user journey from registration to publishing
- Run creation and configuration
- Content collection simulation
- Content review and approval
- Publishing workflow
- Performance validation

**Run Manually**:
```bash
cd deployment
python3 test_e2e_workflow.py
```

**Expected Results**:
- ✅ Complete user workflow functional
- ✅ All major features working together
- ✅ Performance within acceptable limits
- ✅ Error scenarios handled properly

## Development Environment Setup

### Prerequisites

1. **Docker & Docker Compose**: For service orchestration
2. **Python 3.12+**: For running tests
3. **Node.js 18+**: For frontend development
4. **Chrome/Chromium**: For browser testing

### Starting Development Environment

```bash
# Start all services
cd deployment
./start_development.sh

# This will start:
# - PostgreSQL database
# - Redis cache
# - FastAPI backend
# - Celery workers
# - React frontend
```

### Manual Service Startup

If you prefer to start services manually:

```bash
# Backend services
cd backend
docker-compose up -d

# Frontend
cd frontend/multi-source-dashboard
npm install
npm run dev

# Initialize database
cd backend
python scripts/startup.py
```

## Production Testing

### Pre-deployment Validation

```bash
# Run production deployment with testing
cd deployment
./production_deploy.sh --env staging

# Or build and test without deployment
./production_deploy.sh --skip-deployment --run-tests
```

### Load Testing

```bash
# Basic performance testing
cd deployment
python3 -c "
import asyncio
from test_e2e_workflow import E2EWorkflowTester

async def load_test():
    tester = E2EWorkflowTester()
    await tester.test_performance_metrics()

asyncio.run(load_test())
"
```

## Monitoring and Health Checks

### Real-time Monitoring

```bash
# Start continuous monitoring
cd deployment
python3 monitoring.py --mode continuous --interval 30

# Single health check
python3 monitoring.py --mode single --report
```

### Health Check Endpoints

- **Backend Health**: `GET http://localhost:8000/health`
- **API Status**: `GET http://localhost:8000/api/v1/sources/`
- **Task Queue**: `http://localhost:5555` (Flower interface)

## Test Configuration

### Environment Variables

```bash
# Backend URL (default: http://localhost:8000)
export BACKEND_URL=http://localhost:8000

# Frontend URL (default: http://localhost:5173)
export FRONTEND_URL=http://localhost:5173

# Skip frontend tests if frontend not available
export RUN_FRONTEND_TESTS=false

# Generate detailed test reports
export GENERATE_REPORT=true
```

### Test User Credentials

Default test credentials (created during testing):

```
Email: admin@dashboard.local
Password: admin123
```

## Troubleshooting

### Common Issues

1. **Backend Not Responding**
   ```bash
   # Check if services are running
   docker-compose ps
   
   # View logs
   docker-compose logs backend
   ```

2. **Database Connection Issues**
   ```bash
   # Check PostgreSQL status
   docker-compose logs postgres
   
   # Test connection
   psql -h localhost -p 5432 -U dashboard_user -d dashboard_db
   ```

3. **Frontend Not Loading**
   ```bash
   # Check frontend logs
   npm run dev
   
   # Verify API URL in .env
   cat frontend/multi-source-dashboard/.env
   ```

4. **Test Failures**
   ```bash
   # Run tests with verbose output
   python3 test_integration.py -v
   
   # Check test logs
   tail -f monitoring.log
   ```

### Test Data Cleanup

```bash
# Clean test data
cd backend
docker-compose exec postgres psql -U dashboard_user -d dashboard_db -c "
DELETE FROM content WHERE created_at < NOW() - INTERVAL '1 day';
DELETE FROM runs WHERE name LIKE '%test%';
"

# Or reset entire test database
docker-compose down -v
docker-compose up -d
python scripts/startup.py
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Integration Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Start services
      run: |
        cd deployment
        docker-compose -f docker-test-environment.yml up -d
        
    - name: Wait for services
      run: |
        sleep 30
        curl --retry 10 --retry-delay 5 http://localhost:8001/health
        
    - name: Run tests
      run: |
        cd deployment
        docker-compose -f docker-test-environment.yml run test-runner
        
    - name: Cleanup
      run: |
        cd deployment
        docker-compose -f docker-test-environment.yml down -v
```

## Test Results and Reporting

### Generated Files

- **Test Results**: `e2e_test_results.json`, `data_source_test_results.json`, etc.
- **Monitoring Data**: `monitoring_data.json`
- **Test Report**: `test_report_YYYYMMDD_HHMMSS.md`
- **Logs**: `monitoring.log`

### Interpreting Results

- **Green (✅)**: Test passed successfully
- **Yellow (⚠️)**: Test passed with warnings or partial functionality
- **Red (❌)**: Test failed and requires attention

### Performance Benchmarks

Expected performance thresholds:

- **API Response Time**: < 500ms for most endpoints
- **Page Load Time**: < 2 seconds for frontend
- **Database Queries**: < 100ms for simple operations
- **Content Processing**: < 1 second per item
- **System Resource Usage**: < 80% CPU/Memory under normal load

## Support

For issues with integration testing:

1. Check the troubleshooting section above
2. Review test logs and error messages
3. Verify all prerequisites are installed
4. Ensure all services are running and healthy
5. Check network connectivity and firewall settings

The integration testing suite is designed to be comprehensive yet easy to use. It validates all critical functionality and provides clear feedback on system health and readiness for production deployment.