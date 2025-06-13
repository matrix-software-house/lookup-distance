#!/usr/bin/env python3
"""
Test script for the Flask Distance Lookup Service
"""
import requests
import json
import sys
import time

# Service configuration
BASE_URL = "http://localhost:5001"
DISTANCE_ENDPOINT = f"{BASE_URL}/distance"

def test_basic_distance():
    """Test basic distance lookup functionality"""
    print("🧪 Testing basic distance lookup...")
    
    params = {
        'origin': 'New York, NY',
        'destination': 'Boston, MA'
    }
    
    try:
        response = requests.get(DISTANCE_ENDPOINT, params=params)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Success! Distance: {data['rows'][0]['elements'][0]['distance']['text']}")
        print(f"   Duration: {data['rows'][0]['elements'][0]['duration']['text']}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_missing_parameters():
    """Test error handling for missing parameters"""
    print("\n🧪 Testing missing parameters...")
    
    # Test missing destination
    params = {'origin': 'New York, NY'}
    try:
        response = requests.get(DISTANCE_ENDPOINT, params=params)
        if response.status_code == 400:
            print("✅ Correctly returned 400 for missing destination")
        else:
            print(f"❌ Expected 400, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test missing origin
    params = {'destination': 'Boston, MA'}
    try:
        response = requests.get(DISTANCE_ENDPOINT, params=params)
        if response.status_code == 400:
            print("✅ Correctly returned 400 for missing origin")
        else:
            print(f"❌ Expected 400, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_international_locations():
    """Test with international locations"""
    print("\n🧪 Testing international locations...")
    
    params = {
        'origin': 'London, UK',
        'destination': 'Paris, France'
    }
    
    try:
        response = requests.get(DISTANCE_ENDPOINT, params=params)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Success! Distance: {data['rows'][0]['elements'][0]['distance']['text']}")
        print(f"   Duration: {data['rows'][0]['elements'][0]['duration']['text']}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_invalid_locations():
    """Test with invalid locations"""
    print("\n🧪 Testing invalid locations...")
    
    params = {
        'origin': 'InvalidLocation123',
        'destination': 'AnotherInvalidLocation456'
    }
    
    try:
        response = requests.get(DISTANCE_ENDPOINT, params=params)
        data = response.json()
        
        if data.get('status') == 'NOT_FOUND' or data['rows'][0]['elements'][0]['status'] == 'NOT_FOUND':
            print("✅ Correctly handled invalid locations")
        else:
            print(f"⚠️  Unexpected response: {data}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_service_health():
    """Test if service is responsive"""
    print("\n🧪 Testing service health...")
    
    try:
        # Simple health check
        response = requests.get(f"{BASE_URL}/distance", params={'origin': 'test', 'destination': 'test'}, timeout=5)
        print(f"✅ Service is responsive (Status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Service is not accessible")
        return False
    except requests.exceptions.Timeout:
        print("❌ Service is too slow to respond")
        return False
    except Exception as e:
        print(f"⚠️  Service responded with: {e}")
        return True  # Service is up but may have returned an error

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Flask Distance Lookup Service Tests")
    print("=" * 50)
    
    # Check if service is running
    if not test_service_health():
        print("\n❌ Service is not running. Please start it with: docker-compose up")
        return False
    
    # Run all tests
    tests = [
        test_basic_distance,
        test_missing_parameters,
        test_international_locations,
        test_invalid_locations
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"🏁 Tests completed: {passed}/{len(tests)} passed")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
