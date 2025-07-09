#!/bin/bash

# Comprehensive Test Suite Runner for Multi-Source Dashboard
# Runs all integration tests, performance tests, and validation checks

set -e  # Exit on any error

echo "🧪 Multi-Source Dashboard - Complete Test Suite"
echo "==============================================="

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
BACKEND_URL=${BACKEND_URL:-"http://localhost:8000"}
FRONTEND_URL=${FRONTEND_URL:-"http://localhost:5173"}
RUN_FRONTEND_TESTS=${RUN_FRONTEND_TESTS:-"true"}
GENERATE_REPORT=${GENERATE_REPORT:-"true"}
PARALLEL_TESTS=${PARALLEL_TESTS:-"false"}

# Test results tracking
TESTS_PASSED=0
TESTS_FAILED=0
TEST_RESULTS=()

# Function to run a test and track results
run_test() {
    local test_name="$1"
    local test_command="$2"
    local test_description="$3"
    
    print_info "Running: $test_name"
    echo "Description: $test_description"
    echo "Command: $test_command"
    echo ""
    
    start_time=$(date +%s)
    
    if eval "$test_command"; then
        end_time=$(date +%s)
        duration=$((end_time - start_time))
        print_status "$test_name completed successfully (${duration}s)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        TEST_RESULTS+=("✅ $test_name - PASSED (${duration}s)")
    else
        end_time=$(date +%s)
        duration=$((end_time - start_time))
        print_error "$test_name failed (${duration}s)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        TEST_RESULTS+=("❌ $test_name - FAILED (${duration}s)")
    fi
    
    echo ""
}

# Function to check if services are running
check_services() {
    print_info "Checking service availability..."
    
    # Check backend
    if curl -s "$BACKEND_URL/health" > /dev/null; then
        print_status "Backend service is running at $BACKEND_URL"
    else
        print_error "Backend service is not accessible at $BACKEND_URL"
        print_info "Please start the backend service first:"
        print_info "  cd backend && docker-compose up -d"
        exit 1
    fi
    
    # Check frontend (optional)
    if [ "$RUN_FRONTEND_TESTS" = "true" ]; then
        if curl -s "$FRONTEND_URL" > /dev/null; then
            print_status "Frontend service is running at $FRONTEND_URL"
        else
            print_warning "Frontend service is not accessible at $FRONTEND_URL"
            print_info "Some tests will be skipped. To run frontend tests:"
            print_info "  cd frontend/multi-source-dashboard && npm run dev"
            RUN_FRONTEND_TESTS="false"
        fi
    fi
    
    echo ""
}

# Function to install test dependencies
install_dependencies() {
    print_info "Installing test dependencies..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d ".test_env" ]; then
        python3 -m venv .test_env
    fi
    
    # Activate virtual environment
    source .test_env/bin/activate
    
    # Install required packages
    pip install -q httpx pytest selenium beautifulsoup4 requests
    
    print_status "Test dependencies installed"
    echo ""
}

# Run all test categories
run_all_tests() {
    print_info "Starting comprehensive test execution..."
    echo ""
    
    # 1. Backend API Integration Tests
    run_test \
        "Backend API Integration" \
        "cd integration-tests && python3 test_integration.py" \
        "Tests backend API endpoints, authentication, and database connectivity"
    
    # 2. Data Source Integration Tests
    run_test \
        "Data Source Integration" \
        "cd deployment && python3 test_data_sources.py" \
        "Tests Hacker News and Reddit API integrations, content filtering, and scheduling"
    
    # 3. Publishing Integration Tests
    run_test \
        "Publishing Integration" \
        "cd deployment && python3 test_publishing.py" \
        "Tests blog platform APIs, content formatting, and publishing workflows"
    
    # 4. End-to-End Workflow Tests
    run_test \
        "End-to-End Workflow" \
        "cd deployment && python3 test_e2e_workflow.py" \
        "Tests complete user journey from registration to content publishing"
    
    # 5. Frontend-Backend Integration (if frontend is available)
    if [ "$RUN_FRONTEND_TESTS" = "true" ]; then
        run_test \
            "Frontend-Backend Integration" \
            "cd integration-tests && python3 test_frontend_backend.py" \
            "Tests frontend-backend connectivity, UI workflows, and browser compatibility"
    fi
    
    # 6. Backend Unit Tests (if they exist)
    if [ -f "backend/tests/test_basic.py" ]; then
        run_test \
            "Backend Unit Tests" \
            "cd backend && python -m pytest tests/ -v" \
            "Tests individual backend components and business logic"
    fi
    
    # 7. Performance and Load Tests
    run_test \
        "Performance Testing" \
        "cd deployment && python3 -c \"
import asyncio
import httpx
import time

async def performance_test():
    async with httpx.AsyncClient() as client:
        start = time.time()
        tasks = []
        for i in range(10):
            tasks.append(client.get('$BACKEND_URL/health'))
        responses = await asyncio.gather(*tasks)
        end = time.time()
        
        success_count = sum(1 for r in responses if r.status_code == 200)
        print(f'Concurrent requests: {len(tasks)}')
        print(f'Successful responses: {success_count}')
        print(f'Total time: {end - start:.2f}s')
        print(f'Average response time: {(end - start) / len(tasks):.3f}s')
        return success_count == len(tasks)

result = asyncio.run(performance_test())
exit(0 if result else 1)
\"" \
        "Tests system performance under concurrent load"
    
    # 8. Security Tests
    run_test \
        "Security Validation" \
        "cd deployment && python3 -c \"
import httpx
import asyncio

async def security_test():
    async with httpx.AsyncClient() as client:
        # Test unauthorized access
        response = await client.get('$BACKEND_URL/api/v1/users/me')
        if response.status_code != 401:
            print('❌ Unauthorized access not properly blocked')
            return False
            
        # Test invalid auth token
        headers = {'Authorization': 'Bearer invalid_token'}
        response = await client.get('$BACKEND_URL/api/v1/users/me', headers=headers)
        if response.status_code != 401:
            print('❌ Invalid token not properly rejected')
            return False
            
        print('✅ Security validations passed')
        return True

result = asyncio.run(security_test())
exit(0 if result else 1)
\"" \
        "Tests authentication security and unauthorized access protection"
}

# Generate comprehensive test report
generate_test_report() {
    if [ "$GENERATE_REPORT" != "true" ]; then
        return
    fi
    
    print_info "Generating test report..."
    
    report_file="test_report_$(date +%Y%m%d_%H%M%S).md"
    
    cat > "$report_file" << EOF
# Multi-Source Dashboard - Test Report

**Generated:** $(date)
**Backend URL:** $BACKEND_URL
**Frontend URL:** $FRONTEND_URL

## Test Summary

- **Total Tests:** $((TESTS_PASSED + TESTS_FAILED))
- **Passed:** $TESTS_PASSED
- **Failed:** $TESTS_FAILED
- **Success Rate:** $(( TESTS_PASSED * 100 / (TESTS_PASSED + TESTS_FAILED) ))%

## Test Results

EOF

    # Add individual test results
    for result in "${TEST_RESULTS[@]}"; do
        echo "- $result" >> "$report_file"
    done
    
    cat >> "$report_file" << EOF

## Environment Information

- **Backend Health:** $(curl -s "$BACKEND_URL/health" | jq -r '.status' 2>/dev/null || echo "Unknown")
- **Python Version:** $(python3 --version)
- **Test Runner:** $(basename "$0")
- **Operating System:** $(uname -s)

## Test Files Generated

- Backend integration results: \`integration-tests/test_results.json\`
- Data source results: \`deployment/data_source_test_results.json\`
- Publishing results: \`deployment/publishing_test_results.json\`
- E2E workflow results: \`deployment/e2e_test_results.json\`

## Recommendations

EOF

    # Add recommendations based on test results
    if [ $TESTS_FAILED -eq 0 ]; then
        echo "🎉 All tests passed! The application is ready for deployment." >> "$report_file"
    else
        echo "⚠️ Some tests failed. Please review the following:" >> "$report_file"
        echo "" >> "$report_file"
        for result in "${TEST_RESULTS[@]}"; do
            if [[ $result == *"FAILED"* ]]; then
                echo "- Review: ${result#❌ }" >> "$report_file"
            fi
        done
    fi
    
    print_status "Test report generated: $report_file"
}

# Display final summary
show_summary() {
    echo ""
    echo "🏁 Test Suite Execution Complete"
    echo "================================"
    echo ""
    
    if [ $TESTS_FAILED -eq 0 ]; then
        print_status "All tests passed! 🎉"
        echo ""
        print_info "The Multi-Source Dashboard is ready for:"
        echo "  📦 Production deployment"
        echo "  🚀 User acceptance testing"
        echo "  📊 Performance monitoring"
    else
        print_warning "Some tests failed ($TESTS_FAILED/$((TESTS_PASSED + TESTS_FAILED)))"
        echo ""
        print_info "Next steps:"
        echo "  🔍 Review failed tests in the detailed output above"
        echo "  🛠️  Fix identified issues"
        echo "  🔄 Re-run tests with: $0"
    fi
    
    echo ""
    print_info "Test artifacts:"
    echo "  📋 Test report: $(ls test_report_*.md 2>/dev/null | tail -1 || echo 'Not generated')"
    echo "  📊 Result files: integration-tests/ and deployment/ directories"
    echo ""
}

# Cleanup function
cleanup() {
    print_info "Cleaning up test environment..."
    
    # Deactivate virtual environment if active
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate 2>/dev/null || true
    fi
    
    # Remove temporary files if desired
    # rm -f *.tmp 2>/dev/null || true
    
    print_status "Cleanup completed"
}

# Signal handlers
trap cleanup EXIT

# Main execution
main() {
    echo "Test Configuration:"
    echo "  Backend URL: $BACKEND_URL"
    echo "  Frontend URL: $FRONTEND_URL"
    echo "  Frontend Tests: $RUN_FRONTEND_TESTS"
    echo "  Generate Report: $GENERATE_REPORT"
    echo "  Parallel Tests: $PARALLEL_TESTS"
    echo ""
    
    check_services
    install_dependencies
    run_all_tests
    generate_test_report
    show_summary
    
    # Exit with appropriate code
    if [ $TESTS_FAILED -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --backend-url)
            BACKEND_URL="$2"
            shift 2
            ;;
        --frontend-url)
            FRONTEND_URL="$2"
            shift 2
            ;;
        --skip-frontend)
            RUN_FRONTEND_TESTS="false"
            shift
            ;;
        --no-report)
            GENERATE_REPORT="false"
            shift
            ;;
        --parallel)
            PARALLEL_TESTS="true"
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --backend-url URL     Backend service URL (default: http://localhost:8000)"
            echo "  --frontend-url URL    Frontend service URL (default: http://localhost:5173)"
            echo "  --skip-frontend       Skip frontend integration tests"
            echo "  --no-report          Don't generate test report"
            echo "  --parallel           Run tests in parallel (experimental)"
            echo "  --help               Show this help message"
            echo ""
            echo "Environment Variables:"
            echo "  BACKEND_URL          Override backend URL"
            echo "  FRONTEND_URL         Override frontend URL"
            echo "  RUN_FRONTEND_TESTS   Set to 'false' to skip frontend tests"
            echo "  GENERATE_REPORT      Set to 'false' to skip report generation"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Run main function
main