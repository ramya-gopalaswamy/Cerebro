#!/usr/bin/env python3
"""
Live Browser Automation with TinyFish SSE Streaming
Uses /v1/automation/run-sse to get live browser view URL!
"""
import requests
import json
import webbrowser
import os
import dotenv

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# API Keys
TINYFISH_API_KEY = os.environ.get("TINYFISH_API_KEY")
if not TINYFISH_API_KEY:
    raise RuntimeError("TINYFISH_API_KEY not set in environment or .env file.")

TINYFISH_BASE_URL = "https://mino.ai"


def test_tinyfish_sse_live_auto(username: str = "lee215"):
    """
    TinyFish SSE Streaming with auto username - no input needed
    """
    return _run_tinyfish_sse(username)


def test_tinyfish_sse_live():
    """
    TinyFish SSE Streaming - Gets live browser URL!
    Interactive version that asks for username.
    """
    print("\n" + "="*70)
    print("🐟 TINYFISH SSE LIVE BROWSER AUTOMATION")
    print("="*70)
    
    # Let user choose username
    print("\n👤 Enter a LeetCode username to check:")
    print("   (Press Enter for 'lee215' - a famous public profile)")
    username = input("   Username: ").strip() or "lee215"
    
    return _run_tinyfish_sse(username)


def _run_tinyfish_sse(username: str):
    """
    Core TinyFish SSE function
    
    The SSE stream includes:
    - Automation lifecycle events  
    - Browser live-stream URL  <-- We want this!
    - Progress updates  
    - Final results  
    """
    print("\n" + "="*70)
    print("🐟 TINYFISH SSE LIVE BROWSER AUTOMATION")
    print("="*70)
    
    goal = """
    Look at this LeetCode user profile page.
    
    Find and extract:
    1. Total problems solved (the number)
    2. Easy/Medium/Hard breakdown
    3. Recent activity or submissions
    
    Scroll if needed to see more information.
    """
    
    print(f"\n📋 Task: Check LeetCode profile")
    print(f"👤 Username: {username}")
    print(f"🌐 URL: https://leetcode.com/u/{username}/")
    print(f"\n🔗 Endpoint: POST /v1/automation/run-sse")
    print("\n⏳ Starting SSE stream...")
    print("   (Looking for live browser URL in events...)\n")
    
    live_url_opened = False
    
    try:
        # Use SSE streaming endpoint
        response = requests.post(
            f"{TINYFISH_BASE_URL}/v1/automation/run-sse",
            headers={
                "X-API-Key": TINYFISH_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "url": f"https://leetcode.com/u/{username}/",
                "goal": goal,
                "browser_profile": "lite"
            },
            stream=True,  # Enable streaming!
            timeout=180
        )
        
        print(f"📡 Response Status: {response.status_code}")
        print(f"📡 Content-Type: {response.headers.get('content-type')}")
        print("\n" + "-"*70)
        print("📺 SSE EVENTS (watching for live URL):")
        print("-"*70 + "\n")
        
        # Parse SSE events
        event_type = None
        event_data = ""
        
        for line in response.iter_lines(decode_unicode=True):
            if line:
                print(f"   {line}")
                
                # Parse SSE format
                if line.startswith("event:"):
                    event_type = line[6:].strip()
                elif line.startswith("data:"):
                    event_data = line[5:].strip()
                    
                    # Try to parse JSON data
                    try:
                        data = json.loads(event_data)
                        
                        # Look for live browser URL in various fields
                        live_url = (
                            data.get("streamingUrl") or  # TinyFish uses this!
                            data.get("live_stream_url") or 
                            data.get("live_url") or 
                            data.get("browser_url") or
                            data.get("view_url") or
                            data.get("stream_url")
                        )
                        
                        if live_url and not live_url_opened:
                            print(f"\n" + "🎉"*20)
                            print(f"\n   🔴 LIVE BROWSER URL FOUND!")
                            print(f"   {live_url}")
                            print(f"\n   🚀 Opening in your browser...")
                            print(f"\n" + "🎉"*20 + "\n")
                            webbrowser.open(live_url)
                            live_url_opened = True
                        
                        # Check for completion
                        if data.get("status") == "COMPLETED" or event_type == "complete":
                            print(f"\n" + "="*70)
                            print("✅ AUTOMATION COMPLETED!")
                            print("="*70)
                            if data.get("result"):
                                print(f"\n📊 RESULT:")
                                print("-"*50)
                                print(data.get("result"))
                                print("-"*50)
                            return data
                            
                    except json.JSONDecodeError:
                        # Not JSON, might be plain text event
                        if "http" in event_data.lower():
                            print(f"\n   🔗 Possible URL: {event_data}")
                            if not live_url_opened:
                                webbrowser.open(event_data)
                                live_url_opened = True
            
            elif line == "":
                # Empty line = end of event
                event_type = None
                event_data = ""
        
        print("\n" + "="*70)
        print("📡 SSE stream ended")
        print("="*70)
        
        if not live_url_opened:
            print("\n⚠️ No live browser URL was found in the stream")
            print("   TinyFish may not provide live view for this request")
        
        return None
        
    except requests.Timeout:
        print("\n❌ Request timed out after 3 minutes")
        return None
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_tinyfish_sse_simple():
    """
    Simpler test - just print raw SSE output
    """
    print("\n" + "="*70)
    print("🐟 TINYFISH SSE RAW OUTPUT TEST")
    print("="*70)
    
    print("\n⏳ Sending SSE request...")
    
    try:
        response = requests.post(
            f"{TINYFISH_BASE_URL}/v1/automation/run-sse",
            headers={
                "X-API-Key": TINYFISH_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "url": "https://leetcode.com/problemset/",
                "goal": "List the first 3 problem titles you see",
                "browser_profile": "lite"
            },
            stream=True,
            timeout=120
        )
        
        print(f"\n📡 Status: {response.status_code}")
        print(f"📡 Headers: {dict(response.headers)}")
        print("\n📺 RAW SSE OUTPUT:")
        print("-"*70)
        
        for line in response.iter_lines(decode_unicode=True):
            if line:
                print(line)
                
                # Check for URLs
                if "http" in line.lower() and "url" in line.lower():
                    print(f"\n🔗 FOUND URL LINE: {line}\n")
        
        print("-"*70)
        print("\n✅ Stream complete")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import sys
    
    print("\n" + "🎬"*35)
    print("\n   TINYFISH LIVE BROWSER AUTOMATION")
    print("   Using SSE Streaming Endpoint!")
    print("\n" + "🎬"*35)
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        username = sys.argv[1]
        print(f"\n👤 Using username from argument: {username}")
        test_tinyfish_sse_live_auto(username)
    else:
        print("\n\nWhich test?")
        print("  1. Full test (parse SSE, open live URL)")
        print("  2. Simple test (just print raw SSE output)")
        
        try:
            choice = input("\nEnter 1 or 2 (default: 1): ").strip() or "1"
            
            if choice == "2":
                test_tinyfish_sse_simple()
            else:
                test_tinyfish_sse_live()
        except EOFError:
            # Non-interactive mode - run with defaults
            print("\n📌 Running with default settings (lee215)...")
            test_tinyfish_sse_live_auto("lee215")
    
    print("\n" + "="*70)
    print("✅ Test complete!")
    print("="*70)
