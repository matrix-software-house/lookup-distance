#!/usr/bin/env python3
"""
Master test runner for the Flask Distance Lookup Service
This script provides a unified interface to run all available tests.
"""
import subprocess
import sys
import time
import requests
from pathlib import Path

def check_service_health():
    """Check if the service is running and healthy"""
    try:
        response = requests.get("http://localhost:5001/distance", 
                               params={'origin': 'test', 'destination': 'test'}, 
                               timeout=5)
        return True
    except:
        return False

def run_command(command, description):
    """Run a shell command and return the result"""
    print(f"\n🔄 {description}")
    print("=" * 60)
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def main():
    """Main test runner"""
    print("🚀 Flask Distance Lookup Service - Master Test Runner")
    print("=" * 60)
    
    # Check if service is running
    print("🔍 Checking service health...")
    if not check_service_health():
        print("❌ Service is not running or not healthy!")
        print("   Please start the service with: docker-compose up")
        return False
    print("✅ Service is running and healthy!")
    
    # Available tests
    tests = [
        {
            'name': 'Quick curl test',
            'command': 'curl -s "http://localhost:5001/distance?origin=New+York,NY&destination=Boston,MA" | python3 -m json.tool',
            'description': 'Basic API test with curl'
        },
        {
            'name': 'Python test suite',
            'command': 'python3 test_service.py',
            'description': 'Comprehensive Python test suite'
        },
        {
            'name': 'Quick test script',
            'command': './quick_test.sh',
            'description': 'Quick bash test with default locations'
        },
        {
            'name': 'International test',
            'command': './quick_test.sh "London, UK" "Paris, France"',
            'description': 'Test with international locations'
        },
        {
            'name': 'Load test',
            'command': 'python3 load_test.py',
            'description': 'Performance and load testing'
        }
    ]
    
    print(f"\n📋 Available Tests:")
    for i, test in enumerate(tests, 1):
        print(f"   {i}. {test['name']}")
    
    print(f"   A. Run all tests")
    print(f"   Q. Quit")
    
    while True:
        choice = input(f"\n🤔 Choose a test to run (1-{len(tests)}, A, Q): ").strip().upper()
        
        if choice == 'Q':
            print("👋 Goodbye!")
            break
        elif choice == 'A':
            print("\n🏃 Running all tests...")
            success_count = 0
            for test in tests:
                if run_command(test['command'], test['description']):
                    success_count += 1
                    print("✅ Test passed!")
                else:
                    print("❌ Test failed!")
            
            print(f"\n📊 Summary: {success_count}/{len(tests)} tests passed")
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(tests):
            test = tests[int(choice) - 1]
            if run_command(test['command'], test['description']):
                print("✅ Test passed!")
            else:
                print("❌ Test failed!")
        else:
            print("❌ Invalid choice. Please try again.")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Test runner interrupted by user")
    except Exception as e:
        print(f"\n❌ Test runner failed: {e}")
