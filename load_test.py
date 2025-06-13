#!/usr/bin/env python3
"""
Load testing script for the Flask Distance Lookup Service
"""
import asyncio
import aiohttp
import time
import statistics
from urllib.parse import urlencode

# Test configuration
BASE_URL = "http://localhost:5001"
CONCURRENT_REQUESTS = 3
TOTAL_REQUESTS = 10

# Test data
TEST_LOCATIONS = [
    ("New York, NY", "Boston, MA"),
    ("San Francisco, CA", "Los Angeles, CA"),
    ("London, UK", "Paris, France"),
    ("Tokyo, Japan", "Osaka, Japan"),
    ("Sydney, Australia", "Melbourne, Australia"),
    ("Berlin, Germany", "Munich, Germany"),
    ("Chicago, IL", "Detroit, MI"),
    ("Miami, FL", "Orlando, FL"),
]

async def make_request(session, origin, destination):
    """Make a single request to the distance API"""
    params = {'origin': origin, 'destination': destination}
    url = f"{BASE_URL}/distance?" + urlencode(params)
    
    start_time = time.time()
    try:
        async with session.get(url) as response:
            await response.json()
            success = response.status == 200
            response_time = time.time() - start_time
            return success, response_time, response.status
    except Exception as e:
        response_time = time.time() - start_time
        return False, response_time, str(e)

async def run_load_test():
    """Run the load test"""
    print(f"🚀 Starting Load Test")
    print(f"📊 Configuration:")
    print(f"   - Concurrent requests: {CONCURRENT_REQUESTS}")
    print(f"   - Total requests: {TOTAL_REQUESTS}")
    print(f"   - Target URL: {BASE_URL}")
    print("=" * 50)
    
    results = []
    success_count = 0
    error_count = 0
    
    async with aiohttp.ClientSession() as session:
        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
        
        async def limited_request():
            async with semaphore:
                # Choose random test location pair
                import random
                origin, destination = random.choice(TEST_LOCATIONS)
                return await make_request(session, origin, destination)
        
        # Start the test
        start_time = time.time()
        print(f"⏰ Test started at {time.strftime('%H:%M:%S')}")
        
        # Create and run all tasks
        tasks = [limited_request() for _ in range(TOTAL_REQUESTS)]
        completed_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = time.time() - start_time
        
        # Process results
        response_times = []
        status_codes = {}
        
        for result in completed_results:
            if isinstance(result, Exception):
                error_count += 1
            else:
                success, response_time, status = result
                response_times.append(response_time)
                
                if success:
                    success_count += 1
                else:
                    error_count += 1
                
                # Count status codes
                status_codes[status] = status_codes.get(status, 0) + 1
    
    # Calculate statistics
    if response_times:
        avg_response_time = statistics.mean(response_times)
        min_response_time = min(response_times)
        max_response_time = max(response_times)
        median_response_time = statistics.median(response_times)
    else:
        avg_response_time = min_response_time = max_response_time = median_response_time = 0
    
    requests_per_second = TOTAL_REQUESTS / total_time if total_time > 0 else 0
    success_rate = (success_count / TOTAL_REQUESTS) * 100
    
    # Print results
    print(f"\n📈 Load Test Results")
    print("=" * 50)
    print(f"⏱️  Total time: {total_time:.2f} seconds")
    print(f"📊 Requests per second: {requests_per_second:.2f}")
    print(f"✅ Successful requests: {success_count}/{TOTAL_REQUESTS} ({success_rate:.1f}%)")
    print(f"❌ Failed requests: {error_count}")
    print(f"\n⚡ Response Time Statistics:")
    print(f"   - Average: {avg_response_time:.3f}s")
    print(f"   - Median: {median_response_time:.3f}s")
    print(f"   - Min: {min_response_time:.3f}s")
    print(f"   - Max: {max_response_time:.3f}s")
    
    if status_codes:
        print(f"\n📋 Status Code Distribution:")
        for status, count in sorted(status_codes.items()):
            print(f"   - {status}: {count} requests")
    
    print("\n" + "=" * 50)
    
    if success_rate >= 95:
        print("🎉 Load test PASSED! Service is performing well.")
    elif success_rate >= 80:
        print("⚠️  Load test PARTIAL! Service has some performance issues.")
    else:
        print("❌ Load test FAILED! Service has significant performance issues.")

if __name__ == "__main__":
    try:
        asyncio.run(run_load_test())
    except KeyboardInterrupt:
        print("\n🛑 Load test interrupted by user")
    except Exception as e:
        print(f"\n❌ Load test failed: {e}")
