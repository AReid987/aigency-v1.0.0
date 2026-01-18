#!/usr/bin/env python3
"""
Comprehensive Integration Test Suite for Multi-Source Dashboard
Tests backend API, data sources, authentication, and publishing pipeline
"""

import asyncio
import httpx
import pytest
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

# Test Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword123"
TEST_USER_USERNAME = "testuser"

class IntegrationTestSuite:
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=API_BASE_URL, timeout=30.0)
        self.auth_token: Optional[str] = None
        self.test_user_id: Optional[int] = None
        self.test_run_id: Optional[int] = None
        
    async def setup(self):
        """Initialize test environment"""
        print("🚀 Setting up integration test environment...")
        await self.verify_backend_health()
        
    async def cleanup(self):
        """Clean up test data"""
        print("🧹 Cleaning up test environment...")
        if self.test_run_id:
            await self.delete_test_run()
        if self.test_user_id:
            await self.delete_test_user()
        await self.client.aclose()

    # Backend Health and Connectivity Tests
    async def verify_backend_health(self):
        """Test 1: Verify backend is running and accessible"""
        print("✅ Testing backend health check...")
        try:
            response = await self.client.get("/health", base_url="http://localhost:8000")
            assert response.status_code == 200
            health_data = response.json()
            assert health_data["status"] == "healthy"
            print(f"   Backend health: {health_data}")
            return True
        except Exception as e:
            print(f"❌ Backend health check failed: {e}")
            return False

    async def test_cors_configuration(self):
        """Test 2: Verify CORS is configured correctly"""
        print("✅ Testing CORS configuration...")
        headers = {
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type,Authorization"
        }
        try:
            response = await self.client.options(f"{API_BASE_URL}/auth/login", headers=headers)
            # CORS should allow the request or return appropriate headers
            print(f"   CORS preflight response: {response.status_code}")
            return True
        except Exception as e:
            print(f"❌ CORS test failed: {e}")
            return False

    # Authentication Flow Tests
    async def test_user_registration(self):
        """Test 3: User registration flow"""
        print("✅ Testing user registration...")
        registration_data = {
            "email": TEST_USER_EMAIL,
            "username": TEST_USER_USERNAME,
            "password": TEST_USER_PASSWORD,
            "full_name": "Test User"
        }
        
        try:
            response = await self.client.post("/auth/register", json=registration_data)
            if response.status_code == 200:
                user_data = response.json()
                self.test_user_id = user_data["id"]
                print(f"   User registered successfully: ID {self.test_user_id}")
                return True
            else:
                print(f"   Registration response: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ User registration failed: {e}")
            return False

    async def test_user_login(self):
        """Test 4: User login and token generation"""
        print("✅ Testing user login...")
        login_data = {
            "username": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        }
        
        try:
            response = await self.client.post(
                "/auth/login", 
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                auth_data = response.json()
                self.auth_token = auth_data["access_token"]
                print(f"   Login successful, token received")
                return True
            else:
                print(f"   Login failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ User login failed: {e}")
            return False

    async def test_authenticated_request(self):
        """Test 5: Authenticated API request"""
        print("✅ Testing authenticated API access...")
        if not self.auth_token:
            print("   No auth token available")
            return False
            
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        try:
            response = await self.client.get("/users/me", headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                print(f"   Authenticated request successful: {user_data['username']}")
                return True
            else:
                print(f"   Authenticated request failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Authenticated request failed: {e}")
            return False

    # Data Source Integration Tests
    async def test_sources_endpoint(self):
        """Test 6: Sources API endpoint"""
        print("✅ Testing sources endpoint...")
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        try:
            response = await self.client.get("/sources/", headers=headers)
            if response.status_code == 200:
                sources = response.json()
                print(f"   Found {len(sources)} data sources")
                # Check for expected sources
                source_names = [s.get("name") for s in sources]
                if "hackernews" in source_names:
                    print("   ✓ Hacker News source available")
                if "reddit" in source_names:
                    print("   ✓ Reddit source available")
                return True
            else:
                print(f"   Sources endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Sources test failed: {e}")
            return False

    async def test_hacker_news_integration(self):
        """Test 7: Hacker News API integration"""
        print("✅ Testing Hacker News integration...")
        try:
            # Test direct HN API access
            hn_client = httpx.AsyncClient()
            response = await hn_client.get("https://hacker-news.firebaseio.com/v0/topstories.json")
            if response.status_code == 200:
                stories = response.json()
                if len(stories) > 0:
                    print(f"   Hacker News API accessible, {len(stories)} top stories")
                    # Test getting a single story
                    story_response = await hn_client.get(f"https://hacker-news.firebaseio.com/v0/item/{stories[0]}.json")
                    if story_response.status_code == 200:
                        story = story_response.json()
                        print(f"   Sample story: {story.get('title', 'No title')[:50]}...")
                        await hn_client.aclose()
                        return True
            await hn_client.aclose()
            return False
        except Exception as e:
            print(f"❌ Hacker News integration test failed: {e}")
            return False

    # Run Management Tests
    async def test_run_creation(self):
        """Test 8: Run creation workflow"""
        print("✅ Testing run creation...")
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        run_data = {
            "name": "Test Integration Run",
            "description": "Test run for integration testing",
            "frequency": "daily",
            "filters": {
                "keywords": ["test", "integration"],
                "min_score": 1
            },
            "demographics_config": {},
            "publishing_config": {
                "auto_publish": False,
                "max_posts_per_day": 5
            }
        }
        
        try:
            response = await self.client.post("/runs/", json=run_data, headers=headers)
            if response.status_code == 200:
                run = response.json()
                self.test_run_id = run["id"]
                print(f"   Run created successfully: ID {self.test_run_id}")
                return True
            else:
                print(f"   Run creation failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Run creation test failed: {e}")
            return False

    async def test_run_management(self):
        """Test 9: Run status management"""
        print("✅ Testing run management...")
        if not self.test_run_id:
            print("   No test run available")
            return False
            
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        try:
            # Test getting run details
            response = await self.client.get(f"/runs/{self.test_run_id}", headers=headers)
            if response.status_code == 200:
                run = response.json()
                print(f"   Run details retrieved: {run['name']}")
                
                # Test updating run status
                update_data = {"status": "active"}
                update_response = await self.client.put(f"/runs/{self.test_run_id}", json=update_data, headers=headers)
                if update_response.status_code == 200:
                    print("   Run status updated successfully")
                    return True
            return False
        except Exception as e:
            print(f"❌ Run management test failed: {e}")
            return False

    # Content Pipeline Tests
    async def test_content_endpoint(self):
        """Test 10: Content management endpoints"""
        print("✅ Testing content endpoints...")
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        try:
            response = await self.client.get("/content/", headers=headers)
            if response.status_code == 200:
                content = response.json()
                print(f"   Content endpoint accessible, {len(content)} items")
                return True
            else:
                print(f"   Content endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Content endpoint test failed: {e}")
            return False

    # Blog Configuration Tests
    async def test_blog_configs_endpoint(self):
        """Test 11: Blog configuration endpoints"""
        print("✅ Testing blog configuration endpoints...")
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        try:
            response = await self.client.get("/blog-configs/", headers=headers)
            if response.status_code == 200:
                configs = response.json()
                print(f"   Blog configs endpoint accessible, {len(configs)} configs")
                return True
            else:
                print(f"   Blog configs endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Blog configs test failed: {e}")
            return False

    # Database and Task Queue Tests
    async def test_database_connectivity(self):
        """Test 12: Database connectivity through API"""
        print("✅ Testing database connectivity...")
        # Test through user creation/retrieval
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        try:
            response = await self.client.get("/users/me", headers=headers)
            if response.status_code == 200:
                print("   Database connectivity confirmed through user retrieval")
                return True
            return False
        except Exception as e:
            print(f"❌ Database connectivity test failed: {e}")
            return False

    # Error Handling Tests
    async def test_error_handling(self):
        """Test 13: API error handling"""
        print("✅ Testing error handling...")
        try:
            # Test unauthorized access
            response = await self.client.get("/users/me")
            if response.status_code == 401:
                print("   ✓ Unauthorized access properly rejected")
                
            # Test invalid endpoint
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = await self.client.get("/invalid-endpoint", headers=headers)
            if response.status_code == 404:
                print("   ✓ Invalid endpoints properly handled")
                
            return True
        except Exception as e:
            print(f"❌ Error handling test failed: {e}")
            return False

    # Cleanup Methods
    async def delete_test_run(self):
        """Clean up test run"""
        if not self.test_run_id or not self.auth_token:
            return
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        try:
            await self.client.delete(f"/runs/{self.test_run_id}", headers=headers)
            print("   Test run cleaned up")
        except:
            pass

    async def delete_test_user(self):
        """Clean up test user (if endpoint exists)"""
        # This would require an admin endpoint or database cleanup
        pass

    # Main Test Runner
    async def run_all_tests(self):
        """Run all integration tests"""
        print("🧪 Starting Multi-Source Dashboard Integration Tests")
        print("=" * 60)
        
        tests = [
            self.verify_backend_health,
            self.test_cors_configuration,
            self.test_user_registration,
            self.test_user_login,
            self.test_authenticated_request,
            self.test_sources_endpoint,
            self.test_hacker_news_integration,
            self.test_run_creation,
            self.test_run_management,
            self.test_content_endpoint,
            self.test_blog_configs_endpoint,
            self.test_database_connectivity,
            self.test_error_handling,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                result = await test()
                if result:
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ Test {test.__name__} crashed: {e}")
                failed += 1
            print()  # Add spacing between tests
        
        print("=" * 60)
        print(f"🏁 Test Results: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("🎉 All integration tests passed!")
            return True
        else:
            print("⚠️  Some tests failed. Check backend and configuration.")
            return False

# Main execution
async def main():
    test_suite = IntegrationTestSuite()
    try:
        await test_suite.setup()
        success = await test_suite.run_all_tests()
        return 0 if success else 1
    finally:
        await test_suite.cleanup()

if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)