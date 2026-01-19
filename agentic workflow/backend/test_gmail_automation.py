#!/usr/bin/env python3
"""
Gmail Job Email Automation with TinyFish SSE Streaming

This script:
1. Opens Gmail in a live browser view
2. Logs in with user credentials  
3. Searches for job-related emails
4. Extracts: Application confirmations, Interview invites, Rejections
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


def gmail_job_email_automation(email: str, password: str):
    """
    Login to Gmail and extract job-related emails using TinyFish SSE.
    
    Args:
        email: Gmail address
        password: Gmail password (or app password)
    """
    print("\n" + "="*70)
    print("📧 GMAIL JOB EMAIL AUTOMATION")
    print("   Powered by TinyFish Live Browser")
    print("="*70)
    
    goal = f"""
    TASK: Login to Gmail and find specific job-related emails
    
    STEP 1 - LOGIN:
    1. You are on the Gmail login page
    2. Enter the email: {email}
    3. Click "Next" and wait for password field
    4. Enter the password: {password}
    5. Click "Next" to login
    6. Wait for inbox to load completely
    
    STEP 2 - SEARCH FOR SPECIFIC JOB EMAILS:
    After logging in, use the Gmail search bar to search for these SPECIFIC emails.
    
    Search for: "Application Submitted" OR "Interview Scheduled" OR "Update on Your Job Application"
    
    Look for emails with these EXACT subjects:
    1. "Application Submitted Successfully - Infotech Private Limited"
    2. "Application Submitted Successfully - Techstart"
    3. "Update on Your Job Application - XYZ Company Limited"
    4. "Interview Scheduled – Frontend Developer Position (Kinara Private Limited)"
    
    STEP 3 - EXTRACT AND CATEGORIZE:
    Find and categorize each email:
    
    A) APPLICATION CONFIRMATIONS - emails with "Application Submitted Successfully":
       - Infotech Private Limited (Demo)
       - Techstart (Demo)
    
    B) INTERVIEW INVITES - emails with "Interview Scheduled":
       - Kinara Private Limited - Frontend Developer Position
    
    C) APPLICATION UPDATES - emails with "Update on Your Job Application":
       - XYZ Company Limited (could be rejection or update)
    
    RETURN FORMAT (as JSON):
    {{
        "applications": [
            {{"company": "Infotech Private Limited", "subject": "Application Submitted Successfully", "date": "...", "status": "submitted"}},
            {{"company": "Techstart", "subject": "Application Submitted Successfully", "date": "...", "status": "submitted"}}
        ],
        "interviews": [
            {{"company": "Kinara Private Limited", "position": "Frontend Developer", "subject": "Interview Scheduled", "date": "..."}}
        ],
        "updates": [
            {{"company": "XYZ Company Limited", "subject": "Update on Your Job Application", "date": "...", "type": "update"}}
        ],
        "summary": {{
            "total_applications": 2,
            "total_interviews": 1,
            "total_updates": 1
        }}
    }}
    
    Search the inbox thoroughly and find ALL matching emails.
    """
    
    print(f"\n📧 Email: {email}")
    print(f"🔐 Password: {'*' * len(password)}")
    print(f"\n🔗 Endpoint: POST /v1/automation/run-sse")
    print(f"🛡️ Browser Profile: stealth (anti-bot detection)")
    print("\n⏳ Starting Gmail automation...")
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
                "url": "https://accounts.google.com/signin/v2/identifier?service=mail",
                "goal": goal,
                "browser_profile": "stealth"  # Important for Gmail!
            },
            stream=True,
            timeout=300  # 5 minute timeout for login + email reading
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
                            print(f"\n   🚀 Opening browser - WATCH THE LOGIN!")
                            print(f"\n" + "🎉"*20 + "\n")
                            webbrowser.open(streaming_url)
                            live_url_opened = True
                        
                        # Check for completion
                        if data.get("status") == "COMPLETED" or data.get("type") == "COMPLETE":
                            result_data = data
                            print(f"\n" + "="*70)
                            print("✅ GMAIL AUTOMATION COMPLETED!")
                            print("="*70)
                            
                            # Pretty print results
                            if data.get("resultJson"):
                                print_job_emails(data.get("resultJson"))
                            elif data.get("result"):
                                print(f"\n📊 RAW RESULT:")
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


def print_job_emails(result):
    """Pretty print categorized job emails"""
    print(f"\n" + "📬"*25)
    print("\n   JOB EMAIL SUMMARY")
    print("\n" + "📬"*25)
    
    if isinstance(result, dict):
        # Application Confirmations
        apps = result.get("applications") or result.get("application_confirmations") or []
        print(f"\n\n📤 APPLICATION SUBMISSIONS ({len(apps) if isinstance(apps, list) else '?'}):")
        print("-"*50)
        if apps:
            if isinstance(apps, list):
                for email in apps:
                    company = email.get('company', 'Unknown')
                    subject = email.get('subject', 'Application Submitted Successfully')
                    date = email.get('date', 'Unknown date')
                    print(f"   ✅ {company}")
                    print(f"      Subject: {subject}")
                    print(f"      📅 {date}")
                    print()
            else:
                print(f"   {apps}")
        else:
            print("   No application confirmations found")
        
        # Interview Invites
        interviews = result.get("interviews") or result.get("interview_invites") or []
        print(f"\n📅 INTERVIEW SCHEDULED ({len(interviews) if isinstance(interviews, list) else '?'}):")
        print("-"*50)
        if interviews:
            if isinstance(interviews, list):
                for email in interviews:
                    company = email.get('company', 'Unknown')
                    position = email.get('position', email.get('subject', 'Position'))
                    date = email.get('date', 'Unknown date')
                    print(f"   🎯 {company}")
                    print(f"      Position: {position}")
                    print(f"      📅 {date}")
                    print()
            else:
                print(f"   {interviews}")
        else:
            print("   No interview invites found")
        
        # Updates (could be rejection or other updates)
        updates = result.get("updates") or result.get("rejections") or []
        print(f"\n📋 APPLICATION UPDATES ({len(updates) if isinstance(updates, list) else '?'}):")
        print("-"*50)
        if updates:
            if isinstance(updates, list):
                for email in updates:
                    company = email.get('company', 'Unknown')
                    subject = email.get('subject', 'Update on Your Job Application')
                    date = email.get('date', 'Unknown date')
                    update_type = email.get('type', 'update')
                    emoji = "⚠️" if update_type == "rejection" else "📋"
                    print(f"   {emoji} {company}")
                    print(f"      Subject: {subject}")
                    print(f"      📅 {date}")
                    print()
            else:
                print(f"   {updates}")
        else:
            print("   No updates found")
        
        # Summary stats if available
        summary = result.get("summary", {})
        if summary:
            print(f"\n📊 SUMMARY:")
            print("-"*50)
            if isinstance(summary, dict):
                print(f"   Total Applications: {summary.get('total_applications', 0)}")
                print(f"   Total Interviews: {summary.get('total_interviews', 0)}")
                print(f"   Total Updates: {summary.get('total_updates', 0)}")
            else:
                print(f"   {summary}")
    else:
        print(f"\n{result}")


def gmail_search_only(email: str):
    """
    Simpler version - just search Gmail without login (if already logged in)
    """
    print("\n" + "="*70)
    print("📧 GMAIL SEARCH (No Login)")
    print("="*70)
    
    goal = """
    Search this Gmail inbox for job-related emails.
    
    Look for emails with subjects containing:
    - "Application", "Interview", "Offer", "Rejection"
    - Company names (Google, Meta, Amazon, etc.)
    
    List the most recent 10 job-related emails with:
    - Subject
    - From
    - Date
    - Category (Application/Interview/Rejection/Other)
    """
    
    print(f"\n📧 Searching inbox for: {email}")
    print("⏳ Starting search...\n")
    
    try:
        response = requests.post(
            f"{TINYFISH_BASE_URL}/v1/automation/run-sse",
            headers={
                "X-API-Key": TINYFISH_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "url": f"https://mail.google.com/mail/u/0/#search/subject:(application+OR+interview+OR+offer)",
                "goal": goal,
                "browser_profile": "stealth"
            },
            stream=True,
            timeout=180
        )
        
        print(f"📡 Response Status: {response.status_code}\n")
        
        for line in response.iter_lines(decode_unicode=True):
            if line:
                print(f"   {line}")
                
                if line.startswith("data:"):
                    try:
                        data = json.loads(line[5:].strip())
                        
                        if data.get("streamingUrl"):
                            print(f"\n🔴 LIVE VIEW: {data['streamingUrl']}\n")
                            webbrowser.open(data["streamingUrl"])
                            
                        if data.get("status") == "COMPLETED":
                            print(f"\n✅ Search complete!")
                            if data.get("resultJson"):
                                print(json.dumps(data["resultJson"], indent=2))
                            return data
                    except:
                        pass
                        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    print("\n" + "📧"*35)
    print("\n   GMAIL JOB EMAIL AUTOMATION")
    print("   Find Applications, Interviews & Rejections")
    print("\n" + "📧"*35)
    
    # Check command line arguments
    if len(sys.argv) >= 3:
        email = sys.argv[1]
        password = sys.argv[2]
        print(f"\n📧 Using credentials from arguments")
        gmail_job_email_automation(email, password)
    else:
        print("\n\n⚠️  USAGE:")
        print("   python3 test_gmail_automation.py <email> <password>")
        print("\n   Example:")
        print("   python3 test_gmail_automation.py myemail@gmail.com mypassword123")
        print("\n💡 TIP: Use an App Password if you have 2FA enabled")
        print("   https://myaccount.google.com/apppasswords")
        print("\n" + "-"*70)
        
        # Interactive mode
        try:
            print("\nOr enter credentials now:")
            email = input("   📧 Gmail address: ").strip()
            password = input("   🔐 Password: ").strip()
            
            if email and password:
                gmail_job_email_automation(email, password)
            else:
                print("\n❌ Email and password required!")
        except EOFError:
            print("\n❌ No credentials provided. Exiting.")
    
    print("\n" + "="*70)
    print("✅ Script complete!")
    print("="*70)
