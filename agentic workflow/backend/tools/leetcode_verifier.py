"""
LeetCode Verification using TinyFish Browser Automation

This script:
1. Logs into LeetCode with user credentials
2. Checks submission history for specific problems
3. Uses LLM to analyze if submissions were successful
"""
import requests
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
import sys
sys.path.append('..')

from config import TINYFISH_API_KEY, TINYFISH_BASE_URL
from llm_factory import get_agent_llm


@dataclass
class LeetCodeProblem:
    """Problem to verify"""
    title: str
    url: Optional[str] = None
    difficulty: Optional[str] = None


@dataclass 
class VerificationResult:
    """Result of verification"""
    problem: str
    submitted: bool
    accepted: bool
    submission_time: Optional[str] = None
    language: Optional[str] = None
    details: Optional[str] = None


# =============================================================================
# STEP 1: LOGIN TO LEETCODE
# =============================================================================

def tinyfish_leetcode_login(email: str, password: str) -> dict:
    """
    Login to LeetCode using TinyFish browser automation.
    
    Args:
        email: LeetCode email/username
        password: LeetCode password
        
    Returns:
        Session info and login status
    """
    goal = f"""
    TASK: Login to LeetCode
    
    STEPS:
    1. Click on "Sign In" button if visible
    2. Wait for login form to load
    3. Find the email/username input field and enter: {email}
    4. Find the password input field and enter: {password}
    5. Click the "Sign In" or "Login" submit button
    6. Wait for the page to load after login
    7. Verify login was successful by checking if:
       - User avatar/profile icon appears
       - Or username appears in the header
       - Or we're redirected to the home/problems page
    
    IMPORTANT: 
    - Handle any cookie consent popups first
    - Wait for elements to be clickable before interacting
    - Report clearly if login failed (wrong credentials, captcha, etc.)
    
    RETURN: Confirm if login was successful or failed with reason.
    """
    
    print(f"[TinyFish] 🔐 Logging into LeetCode as {email}...")
    
    try:
        response = requests.post(
            f"{TINYFISH_BASE_URL}/v1/automation/run",
            headers={
                "X-API-Key": TINYFISH_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "url": "https://leetcode.com/accounts/login/",
                "goal": goal,
                "browser_profile": "stealth"  # Use stealth for login pages
            },
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        
        print(f"[TinyFish] Login status: {result.get('status')}")
        
        return {
            "success": result.get("status") == "COMPLETED",
            "run_id": result.get("run_id"),
            "result": result.get("result"),
            "error": result.get("error")
        }
        
    except requests.RequestException as e:
        print(f"[TinyFish] Login error: {e}")
        return {"success": False, "error": str(e)}


# =============================================================================
# STEP 2: CHECK SUBMISSIONS FOR SPECIFIC PROBLEMS
# =============================================================================

def tinyfish_check_submissions(
    problems: List[LeetCodeProblem],
    username: str
) -> dict:
    """
    Check if user has submissions for specific LeetCode problems.
    
    Args:
        problems: List of problems to verify
        username: LeetCode username to check
        
    Returns:
        Submission status for each problem
    """
    problems_list = "\n".join([
        f"- {p.title}" + (f" ({p.url})" if p.url else "")
        for p in problems
    ])
    
    goal = f"""
    TASK: Check LeetCode submission history for user '{username}'
    
    PROBLEMS TO VERIFY:
    {problems_list}
    
    STEPS:
    1. Go to the user's profile submissions page
    2. Look at the recent submissions list
    3. For EACH problem in the list above, check if:
       - The user has submitted a solution
       - The submission status (Accepted, Wrong Answer, Time Limit Exceeded, etc.)
       - When the submission was made (today, yesterday, etc.)
       - What programming language was used
    
    4. Return a detailed report for each problem:
       - Problem name
       - Was it submitted? (yes/no)
       - Submission result (Accepted/Failed/Not submitted)
       - Time of submission if available
       - Language used
    
    FORMAT YOUR RESPONSE AS:
    Problem: [name]
    Submitted: Yes/No
    Status: Accepted/Wrong Answer/Not Submitted
    Time: [when]
    Language: [language]
    ---
    (repeat for each problem)
    """
    
    print(f"[TinyFish] 📋 Checking submissions for {len(problems)} problems...")
    
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
            timeout=180
        )
        response.raise_for_status()
        result = response.json()
        
        print(f"[TinyFish] Submission check status: {result.get('status')}")
        
        return {
            "success": result.get("status") == "COMPLETED",
            "run_id": result.get("run_id"),
            "raw_result": result.get("result"),
            "num_steps": result.get("num_of_steps", 0),
            "error": result.get("error")
        }
        
    except requests.RequestException as e:
        print(f"[TinyFish] Submission check error: {e}")
        return {"success": False, "error": str(e)}


# =============================================================================
# STEP 3: USE LLM TO ANALYZE SUBMISSION RESULTS
# =============================================================================

async def analyze_submissions_with_llm(
    raw_result: str,
    problems: List[LeetCodeProblem]
) -> List[VerificationResult]:
    """
    Use LLM to parse and analyze TinyFish submission results.
    
    Args:
        raw_result: Raw text output from TinyFish
        problems: List of problems we were checking
        
    Returns:
        Structured verification results
    """
    problems_json = json.dumps([
        {"title": p.title, "difficulty": p.difficulty}
        for p in problems
    ], indent=2)
    
    prompt = f"""
    Analyze this LeetCode submission verification result and extract structured data.
    
    PROBLEMS WE WERE CHECKING:
    {problems_json}
    
    RAW BROWSER AUTOMATION RESULT:
    {raw_result}
    
    TASK: Parse the result and determine for EACH problem:
    1. Was a submission found? (true/false)
    2. Was the submission accepted/successful? (true/false)
    3. When was it submitted? (if available)
    4. What language was used? (if available)
    5. Any additional details
    
    RESPOND IN EXACT JSON FORMAT:
    {{
        "verifications": [
            {{
                "problem": "Two Sum",
                "submitted": true,
                "accepted": true,
                "submission_time": "2 hours ago",
                "language": "Python3",
                "details": "Solved on first attempt"
            }},
            {{
                "problem": "Add Two Numbers",
                "submitted": false,
                "accepted": false,
                "submission_time": null,
                "language": null,
                "details": "No submission found for this problem"
            }}
        ],
        "summary": {{
            "total_problems": 2,
            "submitted_count": 1,
            "accepted_count": 1,
            "completion_rate": 50
        }}
    }}
    
    If you cannot determine a value, use null. Be conservative - only mark as accepted if clearly stated.
    """
    
    print("[LLM] 🧠 Analyzing submission results...")
    
    llm = get_agent_llm("verifier")
    response = await llm.ainvoke(prompt)
    content = response.content
    
    # Parse JSON from response
    try:
        # Handle markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        parsed = json.loads(content.strip())
        verifications = parsed.get("verifications", [])
        
        results = []
        for v in verifications:
            results.append(VerificationResult(
                problem=v.get("problem", "Unknown"),
                submitted=v.get("submitted", False),
                accepted=v.get("accepted", False),
                submission_time=v.get("submission_time"),
                language=v.get("language"),
                details=v.get("details")
            ))
        
        print(f"[LLM] ✅ Analyzed {len(results)} problem verifications")
        return results
        
    except json.JSONDecodeError as e:
        print(f"[LLM] ⚠️ Failed to parse response: {e}")
        # Return empty results with error
        return [
            VerificationResult(
                problem=p.title,
                submitted=False,
                accepted=False,
                details=f"Analysis failed: {str(e)}"
            )
            for p in problems
        ]


# =============================================================================
# MAIN VERIFICATION FLOW
# =============================================================================

async def verify_daily_leetcode(
    email: str,
    password: str,
    username: str,
    problems: List[Dict]
) -> dict:
    """
    Complete LeetCode verification flow:
    1. Login (optional, for private profiles)
    2. Check submissions for daily problems
    3. Analyze results with LLM
    
    Args:
        email: LeetCode email (optional if profile is public)
        password: LeetCode password (optional if profile is public)
        username: LeetCode username to check
        problems: List of problems from daily plan
        
    Returns:
        Complete verification report
    """
    print("\n" + "="*60)
    print("🎯 LEETCODE DAILY VERIFICATION")
    print("="*60)
    
    # Convert problems to dataclass
    problem_list = [
        LeetCodeProblem(
            title=p.get("title", p.get("name", "Unknown")),
            url=p.get("url"),
            difficulty=p.get("difficulty")
        )
        for p in problems
    ]
    
    print(f"📋 Verifying {len(problem_list)} problems for user: {username}")
    for p in problem_list:
        print(f"   - {p.title} ({p.difficulty or 'unknown difficulty'})")
    
    # Step 1: Login (optional - skip if profile is public)
    login_result = None
    if email and password:
        print("\n🔐 Step 1: Logging in...")
        login_result = tinyfish_leetcode_login(email, password)
        if not login_result.get("success"):
            print(f"⚠️ Login failed: {login_result.get('error')}")
            print("   Continuing with public profile check...")
    else:
        print("\n🔓 Step 1: Skipping login (checking public profile)")
    
    # Step 2: Check submissions
    print("\n📊 Step 2: Checking submissions...")
    submission_result = tinyfish_check_submissions(problem_list, username)
    
    if not submission_result.get("success"):
        return {
            "success": False,
            "error": f"Failed to check submissions: {submission_result.get('error')}",
            "login_status": login_result
        }
    
    # Step 3: Analyze with LLM
    print("\n🧠 Step 3: Analyzing results with LLM...")
    verifications = await analyze_submissions_with_llm(
        submission_result.get("raw_result", ""),
        problem_list
    )
    
    # Calculate summary
    total = len(verifications)
    submitted = sum(1 for v in verifications if v.submitted)
    accepted = sum(1 for v in verifications if v.accepted)
    
    summary = {
        "total_problems": total,
        "submitted_count": submitted,
        "accepted_count": accepted,
        "completion_rate": round((accepted / total) * 100) if total > 0 else 0
    }
    
    print("\n" + "="*60)
    print("📈 VERIFICATION SUMMARY")
    print("="*60)
    print(f"   Total Problems: {total}")
    print(f"   Submitted: {submitted}/{total}")
    print(f"   Accepted: {accepted}/{total}")
    print(f"   Completion Rate: {summary['completion_rate']}%")
    print("="*60 + "\n")
    
    return {
        "success": True,
        "username": username,
        "verifications": [
            {
                "problem": v.problem,
                "submitted": v.submitted,
                "accepted": v.accepted,
                "submission_time": v.submission_time,
                "language": v.language,
                "details": v.details
            }
            for v in verifications
        ],
        "summary": summary,
        "raw_result": submission_result.get("raw_result")
    }


# =============================================================================
# CLI USAGE
# =============================================================================

if __name__ == "__main__":
    import asyncio
    
    # Example usage
    test_problems = [
        {"title": "Two Sum", "difficulty": "Easy", "url": "https://leetcode.com/problems/two-sum/"},
        {"title": "Valid Parentheses", "difficulty": "Easy", "url": "https://leetcode.com/problems/valid-parentheses/"},
        {"title": "Maximum Subarray", "difficulty": "Medium", "url": "https://leetcode.com/problems/maximum-subarray/"}
    ]
    
    async def main():
        result = await verify_daily_leetcode(
            email="",  # Leave empty for public profile
            password="",
            username="demo_user",  # Replace with actual username
            problems=test_problems
        )
        print(json.dumps(result, indent=2))
    
    asyncio.run(main())
