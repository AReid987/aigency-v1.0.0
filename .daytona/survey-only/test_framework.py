#!/usr/bin/env python3
"""
Test script for the Survey Automation Framework
"""

import asyncio
import aiohttp
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_api_endpoints():
    """Test all API endpoints"""
    async with aiohttp.ClientSession() as session:
        print("🧪 Testing Survey Automation Framework API")
        print("=" * 50)
        
        # Test 1: Health check
        print("1. Testing health check...")
        async with session.get(f"{BASE_URL}/") as resp:
            data = await resp.json()
            print(f"   ✅ Health check: {data['message']}")
        
        # Test 2: Get status
        print("\n2. Testing agent status...")
        async with session.get(f"{BASE_URL}/api/status") as resp:
            data = await resp.json()
            print(f"   ✅ Agent status: {data['status']}")
            print(f"   📊 Stats: {data['stats']}")
        
        # Test 3: Get browser options
        print("\n3. Testing browser options...")
        async with session.get(f"{BASE_URL}/api/browser-options") as resp:
            data = await resp.json()
            print(f"   ✅ Available options: {len(data['options'])}")
            for option in data['options']:
                print(f"      - {option['name']}: {option['status']}")
        
        # Test 4: Get live view status
        print("\n4. Testing live view status...")
        async with session.get(f"{BASE_URL}/api/live-view") as resp:
            data = await resp.json()
            print(f"   ✅ Live view available: {data['available']}")
        
        # Test 5: Start a test survey
        print("\n5. Testing survey start...")
        survey_config = {
            "name": "Test Survey",
            "url": "https://example.com/survey",
            "profile": "default",
            "enable_viewing": True,
            "use_ai": False
        }
        
        async with session.post(
            f"{BASE_URL}/api/survey/start", 
            json=survey_config
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                print(f"   ✅ Survey started: {data['message']}")
                if data.get('live_view_url'):
                    print(f"   🔗 Live view: {data['live_view_url']}")
            else:
                print(f"   ❌ Survey start failed: {resp.status}")
        
        # Test 6: Check final status
        print("\n6. Testing final status...")
        async with session.get(f"{BASE_URL}/api/status") as resp:
            data = await resp.json()
            print(f"   ✅ Final status: {data['status']}")
            print(f"   📈 Surveys completed: {data['stats']['surveys_completed']}")
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed!")

def test_scripts_integration():
    """Test integration with your existing scripts"""
    print("\n🔧 Testing Script Integration")
    print("=" * 50)
    
    # Check if scripts exist
    import os
    script_dir = "scripts"
    scripts = [
        "browser_use_script.py",
        "skyvern_script.py", 
        "combined_skyvern_script.py"
    ]
    
    for script in scripts:
        script_path = os.path.join(script_dir, script)
        if os.path.exists(script_path):
            print(f"   ✅ {script} - Found")
            # Check if it's not just a placeholder
            with open(script_path, 'r') as f:
                content = f.read()
                if "TODO" in content or "placeholder" in content.lower():
                    print(f"      ⚠️  Contains placeholder content")
                else:
                    print(f"      ✅ Contains actual implementation")
        else:
            print(f"   ❌ {script} - Not found")

async def main():
    """Main test function"""
    print(f"🚀 Survey Automation Framework Test Suite")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test script integration first
    test_scripts_integration()
    
    # Test API endpoints
    try:
        await test_api_endpoints()
    except aiohttp.ClientConnectorError:
        print("❌ Could not connect to the API server.")
        print("   Make sure the server is running with: pdm run dev")
        return
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return
    
    print("\n💡 Next Steps:")
    print("   1. Set up BrowserBase API key for Stagehand integration")
    print("   2. Test with real survey URLs")
    print("   3. Create Next.js dashboard for live viewing")
    print("   4. Set up Daytona sandbox for cloud testing")

if __name__ == "__main__":
    asyncio.run(main())
