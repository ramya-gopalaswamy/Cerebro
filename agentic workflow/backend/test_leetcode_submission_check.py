#!/usr/bin/env python3
"""
LeetCode Submission Check with TinyFish SSE Streaming

This script:
1. Logs into LeetCode with user credentials
2. Searches for a specific problem
3. Checks the submissions tab for that problem
4. Summarizes if user has submitted a solution
"""
import requests
import json
import webbrowser
import sys
import os
import dotenv

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
TINYFISH_API_KEY = os.environ.get("TINYFISH_API_KEY")
if not TINYFISH_API_KEY:
    raise RuntimeError("TINYFISH_API_KEY not set in environment or .env file.")

TINYFISH_BASE_URL = "https://mino.ai"


def check_leetcode_submission(email: str, password: str, problem_name: str):
    """
    Login to LeetCode, search for a problem, and check submissions.
    
    Args:
        email: LeetCode login email
        password: LeetCode password
        problem_name: Name of the problem to check
    """
    print("\n" + "="*70)
    print("🔍 LEETCODE SUBMISSION CHECK")
    print("   Powered by TinyFish Live Browser")
    print("="*70)
    
    goal = f"""
    TASK: Login to LeetCode and check if user has submitted a solution for a specific problem
    
    STEP 1 - LOGIN:
    1. You are on the LeetCode login page
    2. Click on "Sign In" if needed
    3. Look for Google/Gmail login option OR email login
    4. Enter email: {email}
    5. Enter password: {password}
    6. Complete the login process
    7. Wait for the main page to load
    
    STEP 2 - SEARCH FOR PROBLEM:
    1. Once logged in, find the search bar (usually at the top)
    2. Click on the search bar
    3. Type: {problem_name}
    4. Wait for search results to appear
    5. Click on the problem "{problem_name}" from the results
    
    STEP 3 - CHECK SUBMISSIONS:
    1. Once on the problem page, look for "Submissions" tab
    2. Click on the "Submissions" tab
    3. Check if there are ANY submissions by the user
    4. Look for:
       - Submission status (Accepted, Wrong Answer, etc.)
       - Submission date/time
       - Language used
       - Runtime/Memory if shown
    
    STEP 4 - SUMMARIZE:
    Return a summary in this format:
    {{
        "problem_name": "{problem_name}",
        "user_email": "{email}",
        "has_submissions": true/false,
        "submissions": [
            {{
                "status": "Accepted" or "Wrong Answer" etc,
                "date": "when submitted",
                "language": "Python3" etc,
                "runtime": "if shown",
                "memory": "if shown"
            }}
        ],
        "total_submissions": number,
        "accepted_submissions": number,
        "summary": "Brief summary of findings"
    }}
    
    If NO submissions are found, return:
    {{
        "problem_name": "{problem_name}",
        "has_submissions": false,
        "total_submissions": 0,
        "summary": "No submissions found for this problem"
    }}
    """
    
    print(f"\n📧 Email: {email}")
    print(f"🔐 Password: {'*' * len(password)}")
    print(f"🔍 Problem: {problem_name}")
    print(f"\n🔗 Endpoint: POST /v1/automation/run-sse")
    print(f"🛡️ Browser Profile: stealth")
    print("\n⏳ Starting LeetCode automation...")
    print("   (Watch the browser window for live action!)\n")
    
    live_url_opened = False
    
    try:
        response = requests.post(
            f"{TINYFISH_BASE_URL}/v1/automation/run-sse",
            headers={
                "X-API-Key": TINYFISH_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "url": "https://leetcode.com/accounts/login/",
                "goal": goal,
                "browser_profile": "stealth"  # Use stealth for login
            },
            stream=True,
            timeout=300  # 5 minute timeout
        )
        
        print(f"📡 Response Status: {response.status_code}")
        print(f"📡 Content-Type: {response.headers.get('content-type')}")
        print("\n" + "-"*70)
        print("📺 SSE EVENTS:")
        print("-"*70 + "\n")
        
        result_data = None
        
        for line in response.iter_lines(decode_unicode=True):
            if line:
                print(f"   {line}")
                
                if line.startswith("data:"):
                    event_data = line[5:].strip()
                    
                    try:
                        data = json.loads(event_data)
                        
                        # Look for streaming URL
                        streaming_url = data.get("streamingUrl")
                        if streaming_url and not live_url_opened:
                            print(f"\n" + "🎉"*20)
                            print(f"\n   🔴 LIVE BROWSER VIEW!")
                            print(f"   {streaming_url}")
                            print(f"\n   🚀 Opening browser - WATCH THE AUTOMATION!")
                            print(f"\n" + "🎉"*20 + "\n")
                            webbrowser.open(streaming_url)
                            live_url_opened = True
                        
                        # Check for completion
                        if data.get("status") == "COMPLETED" or data.get("type") == "COMPLETE":
                            result_data = data
                            print(f"\n" + "="*70)
                            print("✅ LEETCODE CHECK COMPLETED!")
                            print("="*70)
                            
                            # Pretty print results
                            if data.get("resultJson"):
                                print_submission_results(data.get("resultJson"))
                            elif data.get("result"):
                                print(f"\n📊 RESULT:")
                                print("-"*50)
                                print(data.get("result"))
                                print("-"*50)
                            
                            return data
                            
                    except json.JSONDecodeError:
                        pass
        
        print("\n" + "="*70)
        print("📡 SSE stream ended")
        print("="*70)
        
        return result_data
        
    except requests.Timeout:
        print("\n❌ Request timed out after 5 minutes")
        return None
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def print_submission_results(result):
    """Pretty print submission check results"""
    print(f"\n" + "📝"*25)
    print("\n   SUBMISSION CHECK RESULTS")
    print("\n" + "📝"*25)
    
    if isinstance(result, dict):
        problem = result.get("problem_name", "Unknown")
        has_subs = result.get("has_submissions", False)
        total = result.get("total_submissions", 0)
        accepted = result.get("accepted_submissions", 0)
        
        print(f"\n🔍 Problem: {problem}")
        print(f"📊 Has Submissions: {'Yes ✅' if has_subs else 'No ❌'}")
        print(f"📈 Total Submissions: {total}")
        print(f"✅ Accepted: {accepted}")
        
        submissions = result.get("submissions", [])
        if submissions:
            print(f"\n📋 SUBMISSION HISTORY:")
            print("-"*50)
            for i, sub in enumerate(submissions, 1):
                status = sub.get("status", "Unknown")
                emoji = "✅" if "Accepted" in status else "❌"
                print(f"\n   {i}. {emoji} {status}")
                if sub.get("date"):
                    print(f"      📅 {sub.get('date')}")
                if sub.get("language"):
                    print(f"      💻 {sub.get('language')}")
                if sub.get("runtime"):
                    print(f"      ⚡ Runtime: {sub.get('runtime')}")
                if sub.get("memory"):
                    print(f"      💾 Memory: {sub.get('memory')}")
        
        summary = result.get("summary", "")
        if summary:
            print(f"\n📝 SUMMARY:")
            print("-"*50)
            print(f"   {summary}")
    else:
        print(f"\n{result}")


if __name__ == "__main__":
    print("\n" + "🔍"*35)
    print("\n   LEETCODE SUBMISSION CHECKER")
    print("   Check if you solved a specific problem")
    print("\n" + "🔍"*35)
    
    # Default values
    email = "gg.ramyaa@gmail.com"
    password = "sriram1996"
    problem = "Regular Expression Matching"
    
    # Check command line arguments
    if len(sys.argv) >= 4:
        email = sys.argv[1]
        password = sys.argv[2]
        problem = " ".join(sys.argv[3:])
    
    print(f"\n📧 Email: {email}")
    print(f"🔍 Problem: {problem}")
    
    # Run the check
    check_leetcode_submission(email, password, problem)
    
    print("\n" + "="*70)
    print("✅ Script complete!")
    print("="*70)
