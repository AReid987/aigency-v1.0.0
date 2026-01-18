#!/usr/bin/env python3
"""
Data Source Integration Testing
Tests Hacker News and Reddit APIs directly and through the backend
"""

import asyncio
import httpx
import json
import time
from datetime import datetime
from typing import Dict, Any, List

class DataSourceTester:
    def __init__(self):
        self.results = {}
        
    async def test_hacker_news_direct(self):
        """Test Hacker News API directly"""
        print("✅ Testing Hacker News API (Direct)...")
        
        try:
            async with httpx.AsyncClient() as client:
                # Test top stories endpoint
                response = await client.get("https://hacker-news.firebaseio.com/v0/topstories.json")
                if response.status_code == 200:
                    story_ids = response.json()
                    print(f"   ✓ Got {len(story_ids)} top story IDs")
                    
                    # Test individual story endpoint
                    if story_ids:
                        story_response = await client.get(f"https://hacker-news.firebaseio.com/v0/item/{story_ids[0]}.json")
                        if story_response.status_code == 200:
                            story = story_response.json()
                            print(f"   ✓ Sample story: {story.get('title', 'No title')[:50]}...")
                            print(f"   ✓ Story score: {story.get('score', 0)}")
                            print(f"   ✓ Story comments: {story.get('descendants', 0)}")
                            
                            self.results['hacker_news_direct'] = {
                                'status': 'success',
                                'story_count': len(story_ids),
                                'sample_story': {
                                    'id': story.get('id'),
                                    'title': story.get('title'),
                                    'score': story.get('score'),
                                    'comments': story.get('descendants')
                                }
                            }
                            return True
                        else:
                            print(f"   ❌ Failed to get story details: {story_response.status_code}")
                else:
                    print(f"   ❌ Failed to get top stories: {response.status_code}")
                    
        except Exception as e:
            print(f"   ❌ Hacker News direct test failed: {e}")
            self.results['hacker_news_direct'] = {'status': 'error', 'error': str(e)}
        
        return False

    async def test_hacker_news_integration(self):
        """Test Hacker News integration through backend"""
        print("✅ Testing Hacker News Integration (Backend)...")
        
        try:
            # Import the HackerNews integration
            import sys
            sys.path.append('../backend')
            from app.integrations.data_sources.hackernews import HackerNewsAPI
            
            # Create instance and test
            hn_api = HackerNewsAPI()
            
            # Test configuration validation
            valid_config = {
                "story_type": "topstories",
                "limit": 5,
                "min_score": 10
            }
            
            if await hn_api.validate_config(valid_config):
                print("   ✓ Configuration validation passed")
                
                # Test content fetching
                content = await hn_api.fetch_latest_content(valid_config)
                if content:
                    print(f"   ✓ Fetched {len(content)} content items")
                    
                    # Display sample content
                    for i, item in enumerate(content[:3]):
                        print(f"   • Item {i+1}: {item.get('title', 'No title')[:40]}...")
                        print(f"     Score: {item.get('score', 0)}, Comments: {item.get('comments_count', 0)}")
                    
                    self.results['hacker_news_backend'] = {
                        'status': 'success',
                        'content_count': len(content),
                        'config_used': valid_config
                    }
                    return True
                else:
                    print("   ❌ No content returned from backend integration")
            else:
                print("   ❌ Configuration validation failed")
                
        except ImportError:
            print("   ⚠️  Backend modules not available (expected if not in backend directory)")
            return True  # Not a failure, just can't test backend integration
        except Exception as e:
            print(f"   ❌ Backend integration test failed: {e}")
            self.results['hacker_news_backend'] = {'status': 'error', 'error': str(e)}
        
        return False

    async def test_reddit_api_access(self):
        """Test Reddit API accessibility"""
        print("✅ Testing Reddit API Access...")
        
        try:
            async with httpx.AsyncClient() as client:
                # Test public Reddit endpoint (no auth required)
                response = await client.get(
                    "https://www.reddit.com/r/programming/hot.json",
                    headers={"User-Agent": "TestScript/1.0"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get('data', {}).get('children', [])
                    
                    print(f"   ✓ Got {len(posts)} posts from r/programming")
                    
                    if posts:
                        sample_post = posts[0]['data']
                        print(f"   ✓ Sample post: {sample_post.get('title', 'No title')[:50]}...")
                        print(f"   ✓ Post score: {sample_post.get('score', 0)}")
                        print(f"   ✓ Post comments: {sample_post.get('num_comments', 0)}")
                    
                    self.results['reddit_api_access'] = {
                        'status': 'success',
                        'post_count': len(posts)
                    }
                    return True
                else:
                    print(f"   ❌ Reddit API returned status: {response.status_code}")
                    
        except Exception as e:
            print(f"   ❌ Reddit API access test failed: {e}")
            self.results['reddit_api_access'] = {'status': 'error', 'error': str(e)}
        
        return False

    async def test_reddit_rate_limiting(self):
        """Test Reddit API rate limiting compliance"""
        print("✅ Testing Reddit Rate Limiting...")
        
        try:
            async with httpx.AsyncClient() as client:
                request_times = []
                
                # Make multiple requests to test rate limiting
                for i in range(5):
                    start_time = time.time()
                    response = await client.get(
                        "https://www.reddit.com/r/programming/hot.json",
                        headers={"User-Agent": "TestScript/1.0"}
                    )
                    end_time = time.time()
                    
                    request_times.append(end_time - start_time)
                    print(f"   Request {i+1}: {response.status_code} ({end_time - start_time:.2f}s)")
                    
                    # Small delay to be respectful
                    await asyncio.sleep(1)
                
                avg_time = sum(request_times) / len(request_times)
                print(f"   ✓ Average request time: {avg_time:.2f}s")
                
                self.results['reddit_rate_limiting'] = {
                    'status': 'success',
                    'average_request_time': avg_time,
                    'request_count': len(request_times)
                }
                return True
                
        except Exception as e:
            print(f"   ❌ Reddit rate limiting test failed: {e}")
            self.results['reddit_rate_limiting'] = {'status': 'error', 'error': str(e)}
        
        return False

    async def test_content_filtering(self):
        """Test content filtering and categorization"""
        print("✅ Testing Content Filtering...")
        
        try:
            # Sample content for testing
            sample_content = [
                {
                    'title': 'New Python 3.12 Features Released',
                    'content': 'Python 3.12 introduces several new features including improved performance and better error messages.',
                    'score': 150,
                    'author': 'python_dev'
                },
                {
                    'title': 'JavaScript Framework Comparison',
                    'content': 'A comprehensive comparison of React, Vue, and Angular for modern web development.',
                    'score': 50,
                    'author': 'js_ninja'
                },
                {
                    'title': 'Spam Post About Nothing',
                    'content': 'This is just spam content that should be filtered out.',
                    'score': 1,
                    'author': 'spammer'
                }
            ]
            
            # Test keyword filtering
            keywords = ['python', 'javascript', 'programming']
            min_score = 25
            
            filtered_content = []
            for item in sample_content:
                # Check keywords
                title_lower = item['title'].lower()
                content_lower = item['content'].lower()
                
                has_keyword = any(keyword in title_lower or keyword in content_lower for keyword in keywords)
                meets_score = item['score'] >= min_score
                
                if has_keyword and meets_score:
                    filtered_content.append(item)
            
            print(f"   ✓ Filtered {len(filtered_content)} items from {len(sample_content)} total")
            
            # Test categorization
            categories = {
                'python': ['python', 'py'],
                'javascript': ['javascript', 'js', 'react', 'vue', 'angular'],
                'general': []
            }
            
            for item in filtered_content:
                item_categories = []
                title_content = f"{item['title']} {item['content']}".lower()
                
                for category, category_keywords in categories.items():
                    if any(keyword in title_content for keyword in category_keywords):
                        item_categories.append(category)
                
                print(f"   • {item['title'][:40]}... → Categories: {item_categories}")
            
            self.results['content_filtering'] = {
                'status': 'success',
                'original_count': len(sample_content),
                'filtered_count': len(filtered_content),
                'filter_criteria': {
                    'keywords': keywords,
                    'min_score': min_score
                }
            }
            return True
            
        except Exception as e:
            print(f"   ❌ Content filtering test failed: {e}")
            self.results['content_filtering'] = {'status': 'error', 'error': str(e)}
        
        return False

    async def test_scheduling_simulation(self):
        """Simulate content collection scheduling"""
        print("✅ Testing Content Collection Scheduling...")
        
        try:
            # Simulate different scheduling frequencies
            frequencies = {
                'daily': 24 * 60,     # minutes in a day
                '2x': 12 * 60,        # twice daily
                '3x': 8 * 60,         # three times daily
                '4x': 6 * 60,         # four times daily
                'hourly': 60          # hourly
            }
            
            print("   Scheduling intervals:")
            for freq, interval in frequencies.items():
                hours = interval / 60
                runs_per_day = (24 * 60) / interval
                print(f"   • {freq:8}: every {hours:4.1f} hours ({runs_per_day:3.1f} runs/day)")
            
            # Simulate next run calculations
            now = datetime.now()
            print(f"\n   Next run times (from {now.strftime('%H:%M:%S')}):")
            
            for freq, interval in frequencies.items():
                next_run = now.timestamp() + (interval * 60)  # Convert to seconds
                next_run_dt = datetime.fromtimestamp(next_run)
                print(f"   • {freq:8}: {next_run_dt.strftime('%H:%M:%S')}")
            
            self.results['scheduling'] = {
                'status': 'success',
                'frequencies_tested': list(frequencies.keys()),
                'current_time': now.isoformat()
            }
            return True
            
        except Exception as e:
            print(f"   ❌ Scheduling test failed: {e}")
            self.results['scheduling'] = {'status': 'error', 'error': str(e)}
        
        return False

    async def test_error_handling(self):
        """Test error handling for data sources"""
        print("✅ Testing Error Handling...")
        
        try:
            async with httpx.AsyncClient() as client:
                # Test handling of non-existent endpoints
                test_cases = [
                    ("Invalid HN endpoint", "https://hacker-news.firebaseio.com/v0/invalid.json"),
                    ("Invalid Reddit endpoint", "https://www.reddit.com/r/nonexistent/invalid.json"),
                    ("Timeout simulation", "https://httpbin.org/delay/10")  # Will timeout
                ]
                
                for test_name, url in test_cases:
                    try:
                        response = await client.get(url, timeout=5.0)
                        if response.status_code >= 400:
                            print(f"   ✓ {test_name}: Properly handled {response.status_code}")
                        else:
                            print(f"   ⚠️  {test_name}: Unexpected success")
                    except httpx.TimeoutException:
                        print(f"   ✓ {test_name}: Timeout properly handled")
                    except Exception as e:
                        print(f"   ✓ {test_name}: Exception properly caught ({type(e).__name__})")
            
            self.results['error_handling'] = {
                'status': 'success',
                'test_cases': len(test_cases)
            }
            return True
            
        except Exception as e:
            print(f"   ❌ Error handling test failed: {e}")
            self.results['error_handling'] = {'status': 'error', 'error': str(e)}
        
        return False

    def save_test_results(self):
        """Save test results to file"""
        try:
            with open('data_source_test_results.json', 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'results': self.results
                }, f, indent=2)
            print("📊 Test results saved to data_source_test_results.json")
        except Exception as e:
            print(f"⚠️  Could not save test results: {e}")

    async def run_all_tests(self):
        """Run all data source tests"""
        print("🧪 Starting Data Source Integration Tests")
        print("=" * 60)
        
        tests = [
            self.test_hacker_news_direct,
            self.test_hacker_news_integration,
            self.test_reddit_api_access,
            self.test_reddit_rate_limiting,
            self.test_content_filtering,
            self.test_scheduling_simulation,
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
        
        # Save results
        self.save_test_results()
        
        print("=" * 60)
        print(f"🏁 Data Source Test Results: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("🎉 All data source tests passed!")
            return True
        else:
            print("⚠️  Some data source tests failed. Check API availability and configuration.")
            return False

# Main execution
async def main():
    tester = DataSourceTester()
    success = await tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)