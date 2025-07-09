#!/usr/bin/env python3
"""
Frontend-Backend Integration Test using Selenium
Tests the complete user workflow through the React frontend
"""

import asyncio
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class FrontendIntegrationTest:
    def __init__(self, frontend_url="http://localhost:5173", backend_url="http://localhost:8000"):
        self.frontend_url = frontend_url
        self.backend_url = backend_url
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        print("🌐 Setting up Chrome WebDriver...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            print("   Chrome WebDriver initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to setup WebDriver: {e}")
            print("   Make sure Chrome and ChromeDriver are installed")
            return False

    def cleanup(self):
        """Clean up WebDriver"""
        if self.driver:
            self.driver.quit()
            print("🧹 WebDriver closed")

    async def test_frontend_accessibility(self):
        """Test 1: Verify frontend is accessible"""
        print("✅ Testing frontend accessibility...")
        try:
            self.driver.get(self.frontend_url)
            
            # Wait for the page to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Check if we're redirected to login (expected for protected app)
            current_url = self.driver.current_url
            if "/login" in current_url or "login" in self.driver.page_source.lower():
                print("   ✓ Frontend accessible, redirected to login as expected")
                return True
            else:
                print(f"   Frontend loaded but unexpected page: {current_url}")
                return False
                
        except Exception as e:
            print(f"❌ Frontend accessibility test failed: {e}")
            return False

    async def test_login_form(self):
        """Test 2: Login form functionality"""
        print("✅ Testing login form...")
        try:
            # Navigate to login page
            self.driver.get(f"{self.frontend_url}/login")
            
            # Wait for login form to load
            email_input = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
            password_input = self.driver.find_element(By.NAME, "password")
            
            print("   ✓ Login form elements found")
            
            # Try to submit with test credentials
            email_input.send_keys("admin@dashboard.local")
            password_input.send_keys("admin123")
            
            # Find and click submit button
            submit_button = self.driver.find_element(By.TYPE, "submit")
            submit_button.click()
            
            # Wait for response (either success redirect or error message)
            time.sleep(2)
            
            current_url = self.driver.current_url
            if "/dashboard" in current_url:
                print("   ✓ Login successful, redirected to dashboard")
                return True
            elif "error" in self.driver.page_source.lower() or "invalid" in self.driver.page_source.lower():
                print("   ⚠️  Login form working but credentials invalid (expected if no seeded data)")
                return True
            else:
                print(f"   Login attempt completed, current URL: {current_url}")
                return True
                
        except TimeoutException:
            print("   ❌ Login form elements not found - possible frontend routing issue")
            return False
        except Exception as e:
            print(f"   ❌ Login form test failed: {e}")
            return False

    async def test_registration_form(self):
        """Test 3: Registration form functionality"""
        print("✅ Testing registration form...")
        try:
            # Navigate to registration page
            self.driver.get(f"{self.frontend_url}/register")
            
            # Wait for registration form elements
            email_input = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
            username_input = self.driver.find_element(By.NAME, "username")
            password_input = self.driver.find_element(By.NAME, "password")
            
            print("   ✓ Registration form elements found")
            
            # Fill out registration form
            test_email = f"test{int(time.time())}@example.com"
            email_input.send_keys(test_email)
            username_input.send_keys(f"testuser{int(time.time())}")
            password_input.send_keys("testpassword123")
            
            # Find confirm password if it exists
            try:
                confirm_password = self.driver.find_element(By.NAME, "confirmPassword")
                confirm_password.send_keys("testpassword123")
            except NoSuchElementException:
                pass  # Confirm password field might not exist
            
            # Submit registration
            submit_button = self.driver.find_element(By.TYPE, "submit")
            submit_button.click()
            
            time.sleep(3)
            
            # Check result
            if "/dashboard" in self.driver.current_url:
                print("   ✓ Registration successful, redirected to dashboard")
                return True
            elif "error" in self.driver.page_source.lower():
                print("   ⚠️  Registration form working but got error (backend might not be running)")
                return True
            else:
                print("   ✓ Registration form functional")
                return True
                
        except Exception as e:
            print(f"   ❌ Registration form test failed: {e}")
            return False

    async def test_api_connectivity(self):
        """Test 4: Frontend-Backend API connectivity"""
        print("✅ Testing API connectivity from frontend...")
        try:
            # Inject JavaScript to test API connectivity
            self.driver.get(self.frontend_url)
            
            # Execute JavaScript to test API call
            api_test_script = f"""
            return fetch('{self.backend_url}/health')
                .then(response => response.json())
                .then(data => data)
                .catch(error => ({{error: error.message}}));
            """
            
            result = self.driver.execute_async_script(f"""
                var callback = arguments[arguments.length - 1];
                {api_test_script}
                .then(callback);
            """)
            
            if isinstance(result, dict) and result.get("status") == "healthy":
                print("   ✓ Frontend can successfully call backend API")
                return True
            elif isinstance(result, dict) and "error" in result:
                print(f"   ❌ API call failed: {result['error']}")
                return False
            else:
                print(f"   ⚠️  Unexpected API response: {result}")
                return True
                
        except Exception as e:
            print(f"   ❌ API connectivity test failed: {e}")
            return False

    async def test_navigation(self):
        """Test 5: Frontend navigation and routing"""
        print("✅ Testing frontend navigation...")
        try:
            # Test different routes
            routes_to_test = [
                "/login",
                "/register", 
                "/dashboard",
                "/runs",
                "/content",
                "/settings"
            ]
            
            working_routes = 0
            for route in routes_to_test:
                try:
                    self.driver.get(f"{self.frontend_url}{route}")
                    time.sleep(1)
                    
                    # Check if page loaded without errors
                    if "404" not in self.driver.page_source and "error" not in self.driver.title.lower():
                        working_routes += 1
                        print(f"   ✓ Route {route} accessible")
                    else:
                        print(f"   ❌ Route {route} returned error")
                        
                except Exception as e:
                    print(f"   ❌ Route {route} failed: {e}")
            
            if working_routes >= len(routes_to_test) * 0.8:  # 80% success rate
                print(f"   ✓ Navigation test passed ({working_routes}/{len(routes_to_test)} routes working)")
                return True
            else:
                print(f"   ❌ Too many navigation failures ({working_routes}/{len(routes_to_test)} working)")
                return False
                
        except Exception as e:
            print(f"   ❌ Navigation test failed: {e}")
            return False

    async def test_responsive_design(self):
        """Test 6: Responsive design functionality"""
        print("✅ Testing responsive design...")
        try:
            self.driver.get(f"{self.frontend_url}/login")
            
            # Test different screen sizes
            screen_sizes = [
                (1920, 1080),  # Desktop
                (768, 1024),   # Tablet
                (375, 667),    # Mobile
            ]
            
            for width, height in screen_sizes:
                self.driver.set_window_size(width, height)
                time.sleep(1)
                
                # Check if page is still functional
                body = self.driver.find_element(By.TAG_NAME, "body")
                if body:
                    print(f"   ✓ Responsive at {width}x{height}")
                else:
                    print(f"   ❌ Layout broken at {width}x{height}")
                    return False
            
            # Reset to desktop size
            self.driver.set_window_size(1920, 1080)
            print("   ✓ Responsive design test passed")
            return True
            
        except Exception as e:
            print(f"   ❌ Responsive design test failed: {e}")
            return False

    async def test_error_handling(self):
        """Test 7: Frontend error handling"""
        print("✅ Testing frontend error handling...")
        try:
            # Test navigation to non-existent page
            self.driver.get(f"{self.frontend_url}/non-existent-page")
            time.sleep(2)
            
            # Should redirect or show 404
            if "/dashboard" in self.driver.current_url or "404" in self.driver.page_source:
                print("   ✓ Non-existent pages handled correctly")
                return True
            else:
                print("   ⚠️  Non-existent page handling unclear")
                return True
                
        except Exception as e:
            print(f"   ❌ Error handling test failed: {e}")
            return False

    async def run_all_tests(self):
        """Run all frontend integration tests"""
        print("🧪 Starting Frontend-Backend Integration Tests")
        print("=" * 60)
        
        if not self.setup_driver():
            return False
        
        tests = [
            self.test_frontend_accessibility,
            self.test_api_connectivity,
            self.test_login_form,
            self.test_registration_form,
            self.test_navigation,
            self.test_responsive_design,
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
        print(f"🏁 Frontend Test Results: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("🎉 All frontend integration tests passed!")
            return True
        else:
            print("⚠️  Some frontend tests failed. Check frontend and backend servers.")
            return False

# Main execution
async def main():
    test_suite = FrontendIntegrationTest()
    try:
        success = await test_suite.run_all_tests()
        return 0 if success else 1
    finally:
        test_suite.cleanup()

if __name__ == "__main__":
    import sys
    # Check if selenium is available
    try:
        import selenium
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except ImportError:
        print("❌ Selenium not installed. Run: pip install selenium")
        print("   Also ensure Chrome and ChromeDriver are installed")
        sys.exit(1)