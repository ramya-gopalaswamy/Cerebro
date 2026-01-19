#!/usr/bin/env python3
"""
Direct TinyFish API test - simple and verbose
"""
import requests
import json
import os
import dotenv

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

TINYFISH_API_KEY = os.environ.get("TINYFISH_API_KEY")
if not TINYFISH_API_KEY:
    raise RuntimeError("TINYFISH_API_KEY not set in environment or .env file.")

TINYFISH_BASE_URL = "https://mino.ai"

def test_leetcode_profile():
    """Simple test: Check a public LeetCode profile"""
    
    username = "neal_wu"  # Famous competitive programmer
    
    goal = """
    Go to this LeetCode user profile page.
    
    Extract the following information:
    1. Total problems solved (if visible)
    2. Easy/Medium/Hard breakdown (if visible)
    3. Recent submissions or activity (last 3-5 problems)
    
    Return what you find about this user's LeetCode activity.
    """
    
    print("="*60)
    print("🧪 TINYFISH DIRECT API TEST")
    print("="*60)
    print(f"URL: https://leetcode.com/u/{username}/")
    print(f"Goal: Check profile and submissions")
    print("="*60)
    print("\n⏳ Sending request to TinyFish API...")
    print("   (This may take 1-2 minutes for browser automation)\n")
    
    try:
        response = requests.post(
            f"{TINYFISH_BASE_URL}/v1/automation/run",
            headers={
                "X-API-Key": TINYFISH_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "url": f"https://leetcode.com/u/{username}/",
                "goal": goal,
                "browser_profile": "lite"
            },
            timeout=180  # 3 minute timeout
        )
        
        print(f"📡 Response Status Code: {response.status_code}")
        
        result = response.json()
        
        print("\n" + "="*60)
        print("📊 TINYFISH RESPONSE")
        print("="*60)
        print(f"Status: {result.get('status')}")
        print(f"Run ID: {result.get('run_id')}")
        print(f"Steps: {result.get('num_of_steps', 'N/A')}")
        
        if result.get('error'):
            print(f"\n❌ Error: {result.get('error')}")
        
        if result.get('result'):
            print(f"\n✅ Result:")
            print("-"*40)
            print(result.get('result'))
            print("-"*40)
        
        print("\n📦 Full Response:")
        print(json.dumps(result, indent=2))
        
        return result
        
    except requests.Timeout:
        print("❌ Request timed out after 180 seconds")
        return None
    except requests.RequestException as e:
        print(f"❌ Request error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    print("\n🚀 Starting TinyFish test...\n")
    result = test_leetcode_profile()
    print("\n✅ Test complete!")
