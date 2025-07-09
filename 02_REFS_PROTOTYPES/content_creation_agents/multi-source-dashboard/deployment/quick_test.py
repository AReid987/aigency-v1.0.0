#!/usr/bin/env python3
"""
Quick Integration Test - Fast validation of core functionality
Runs essential tests in minimal time for rapid feedback
"""

import asyncio
import httpx
import time
from datetime import datetime

class QuickTester:
    def __init__(self, backend_url="http://localhost:8000", frontend_url="http://localhost:5173"):
        self.backend_url = backend_url
        self.frontend_url = frontend_url
        self.client = httpx.AsyncClient(timeout=10.0)
        
    async def cleanup(self):
        await self.client.aclose()

    async def test_backend_health(self):
        """Quick backend health check"""
        try:
            start = time.time()
            response = await self.client.get(f"{self.backend_url}/health")
            duration = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Backend healthy ({duration:.3f}s): {data.get('status', 'unknown')}")
                return True
            else:
                print(f"❌ Backend unhealthy: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Backend connection failed: {e}")
            return False

    async def test_frontend_access(self):
        """Quick frontend accessibility check"""
        try:
            start = time.time()
            response = await self.client.get(self.frontend_url)
            duration = time.time() - start
            
            if response.status_code == 200:
                print(f"✅ Frontend accessible ({duration:.3f}s)")
                return True
            else:
                print(f"❌ Frontend error: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Frontend connection failed: {e}")
            return False

    async def test_api_endpoints(self):
        """Quick API endpoint validation"""
        endpoints = [
            "/api/v1/sources/",
            "/api/v1/auth/login",
            "/docs"
        ]
        
        success_count = 0
        for endpoint in endpoints:
            try:
                response = await self.client.get(f"{self.backend_url}{endpoint}")
                if response.status_code in [200, 401, 422]:  # 401/422 are acceptable for some endpoints
                    success_count += 1
                    print(f"✅ {endpoint} - {response.status_code}")
                else:
                    print(f"❌ {endpoint} - {response.status_code}")
            except Exception as e:
                print(f"❌ {endpoint} - Error: {e}")
        
        return success_count == len(endpoints)

    async def test_external_apis(self):
        """Quick external API connectivity check"""
        apis = [
            ("Hacker News", "https://hacker-news.firebaseio.com/v0/maxitem.json"),
            ("Dev.to", "https://dev.to/api/articles?per_page=1")
        ]
        
        success_count = 0
        for name, url in apis:
            try:
                start = time.time()
                response = await self.client.get(url)
                duration = time.time() - start
                
                if response.status_code == 200:
                    success_count += 1
                    print(f"✅ {name} API ({duration:.3f}s)")
                else:
                    print(f"❌ {name} API - HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ {name} API - Error: {e}")
        
        return success_count >= len(apis) * 0.8  # 80% success rate

    async def run_quick_tests(self):
        """Run all quick tests"""
        print("🚀 Quick Integration Test Suite")
        print("=" * 40)
        print(f"Backend: {self.backend_url}")
        print(f"Frontend: {self.frontend_url}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        tests = [
            ("Backend Health", self.test_backend_health),
            ("Frontend Access", self.test_frontend_access),
            ("API Endpoints", self.test_api_endpoints),
            ("External APIs", self.test_external_apis),
        ]
        
        passed = 0
        total = len(tests)
        start_time = time.time()
        
        for test_name, test_func in tests:
            print(f"🔄 {test_name}...")
            try:
                if await test_func():
                    passed += 1
                else:
                    print(f"   Test failed")
            except Exception as e:
                print(f"   Test crashed: {e}")
            print()
        
        total_time = time.time() - start_time
        success_rate = (passed / total) * 100
        
        print("=" * 40)
        print(f"📊 Results: {passed}/{total} passed ({success_rate:.1f}%)")
        print(f"⏱️  Duration: {total_time:.2f} seconds")
        
        if passed == total:
            print("🎉 All quick tests passed!")
            print("✅ System ready for detailed testing")
        elif passed >= total * 0.8:
            print("⚠️  Most tests passed - system likely functional")
            print("🔍 Run full test suite for complete validation")
        else:
            print("❌ Multiple test failures detected")
            print("🛠️  Check service status and configuration")
        
        return passed == total

async def main():
    import sys
    
    # Parse simple arguments
    backend_url = "http://localhost:8000"
    frontend_url = "http://localhost:5173"
    
    if len(sys.argv) > 1:
        backend_url = sys.argv[1]
    if len(sys.argv) > 2:
        frontend_url = sys.argv[2]
    
    tester = QuickTester(backend_url, frontend_url)
    try:
        success = await tester.run_quick_tests()
        return 0 if success else 1
    finally:
        await tester.cleanup()

if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)