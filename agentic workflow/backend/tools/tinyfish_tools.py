"""
TinyFish API Tools
- LeetCode problem recommendations
- LeetCode profile verification
- Gmail sent folder checking
"""
import requests
import json
from typing import List, Optional, AsyncGenerator
from langchain_core.tools import tool
import sys
sys.path.append('..')

from config import TINYFISH_API_KEY, TINYFISH_BASE_URL


# =============================================================================
# LEETCODE PROBLEMS - Get recommended problems based on skill level
# =============================================================================

@tool
def tinyfish_get_leetcode_problems(
    difficulty: str = "medium",
    topics: List[str] = None,
    count: int = 5
) -> dict:
    """
    Get LeetCode problem recommendations using TinyFish browser automation.
    Browses LeetCode problem list and extracts relevant problems.
    
    Args:
        difficulty: "easy", "medium", or "hard"
        topics: List of topics like ["arrays", "strings", "dynamic-programming"]
        count: Number of problems to recommend
        
    Returns:
        List of recommended LeetCode problems with links
    """
    topics = topics or ["array", "string", "hash-table"]
    topics_str = ", ".join(topics[:3])
    
    goal = f"""
    I need to find {count} LeetCode problems for interview preparation.
    
    Requirements:
    - Difficulty: {difficulty}
    - Topics: {topics_str}
    
    For each problem found, extract:
    1. Problem number and title
    2. Difficulty level
    3. The problem URL
    4. Main topic/category
    5. Acceptance rate if visible
    
    Return exactly {count} problems that match these criteria.
    """
    
    # Build URL with filters
    topic_filter = topics[0].lower().replace(" ", "-") if topics else "array"
    start_url = f"https://leetcode.com/problemset/?difficulty={difficulty.upper()}&topicSlugs={topic_filter}"
    
    print(f"[TinyFish] Getting {count} {difficulty} LeetCode problems on {topics_str}...")
    
    try:
        response = requests.post(
            f"{TINYFISH_BASE_URL}/v1/automation/run",
            headers={
                "X-API-Key": TINYFISH_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "url": start_url,
                "goal": goal,
                "browser_profile": "lite"
            },
            timeout=180
        )
        response.raise_for_status()
        result = response.json()
        
        print(f"[TinyFish] LeetCode search status: {result.get('status')}")
        
        if result.get("status") == "COMPLETED":
            return {
                "success": True,
                "source": "leetcode",
                "difficulty": difficulty,
                "topics": topics,
                "problems": result.get("result"),
                "run_id": result.get("run_id"),
                "num_steps": result.get("num_of_steps", 0)
            }
        else:
            return {
                "success": False,
                "source": "leetcode",
                "error": result.get("error"),
                "status": result.get("status")
            }
            
    except requests.Timeout:
        print(f"[TinyFish] LeetCode search timed out")
        return {
            "success": False,
            "source": "leetcode",
            "error": "Request timed out after 180 seconds"
        }
    except requests.RequestException as e:
        print(f"[TinyFish] LeetCode search error: {e}")
        return {
            "success": False,
            "source": "leetcode",
            "error": str(e)
        }


# =============================================================================
# LEETCODE VERIFICATION - Check user's submission history
# =============================================================================

@tool
def tinyfish_verify_leetcode(username: str) -> dict:
    """
    Verify LeetCode submissions using TinyFish browser automation.
    Navigates to user's profile and extracts recent activity.
    
    Args:
        username: LeetCode username to check
        
    Returns:
        Dictionary with verification results including problems solved
    """
    goal = f"""
    Go to the LeetCode profile page for user '{username}'.
    
    Find and extract:
    1. Total problems solved (Easy, Medium, Hard breakdown)
    2. Recent submissions or activity (last 5 problems solved with names)
    3. Current streak or consistency data if visible
    4. Ranking if available
    
    Summarize what you find about their LeetCode activity.
    """
    
    print(f"[TinyFish] Verifying LeetCode for user: {username}")
    
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
        
        print(f"[TinyFish] LeetCode verification status: {result.get('status')}")
        
        return {
            "success": result.get("status") == "COMPLETED",
            "source": "leetcode",
            "username": username,
            "run_id": result.get("run_id"),
            "result": result.get("result"),
            "num_steps": result.get("num_of_steps", 0),
            "error": result.get("error")
        }
        
    except requests.Timeout:
        print(f"[TinyFish] LeetCode verification timed out")
        return {
            "success": False,
            "source": "leetcode",
            "username": username,
            "error": "Request timed out after 180 seconds"
        }
    except requests.RequestException as e:
        print(f"[TinyFish] LeetCode verification error: {e}")
        return {
            "success": False,
            "source": "leetcode", 
            "username": username,
            "error": str(e)
        }


# =============================================================================
# GMAIL CHECK - Verify job applications sent
# =============================================================================

@tool
def tinyfish_check_gmail_sent(keywords: Optional[List[str]] = None) -> dict:
    """
    Check Gmail sent folder for job application emails using TinyFish.
    Uses stealth mode for Gmail authentication.
    
    Args:
        keywords: Keywords to search for (default: Application, Resume, etc.)
        
    Returns:
        Dictionary with count of applications and details
    """
    keywords = keywords or ["Application", "Resume", "Cover Letter", "Position", "Job", "Apply"]
    keywords_str = ", ".join(keywords)
    
    goal = f"""
    Check the Gmail Sent folder.
    
    Look for emails sent in the last 24 hours that appear to be job applications.
    Search for keywords: {keywords_str}
    
    For each application email found, note:
    - Recipient email or company name
    - Subject line
    - Approximate time sent
    
    Count the total number of job application emails sent today.
    Return a summary of applications found.
    """
    
    print(f"[TinyFish] Checking Gmail for job applications...")
    
    try:
        response = requests.post(
            f"{TINYFISH_BASE_URL}/v1/automation/run",
            headers={
                "X-API-Key": TINYFISH_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "url": "https://mail.google.com/mail/u/0/#sent",
                "goal": goal,
                "browser_profile": "stealth"  # Anti-detection for Gmail
            },
            timeout=180
        )
        response.raise_for_status()
        result = response.json()
        
        print(f"[TinyFish] Gmail check status: {result.get('status')}")
        
        return {
            "success": result.get("status") == "COMPLETED",
            "source": "gmail",
            "run_id": result.get("run_id"),
            "result": result.get("result"),
            "num_steps": result.get("num_of_steps", 0),
            "error": result.get("error")
        }
        
    except requests.Timeout:
        return {
            "success": False,
            "source": "gmail",
            "error": "Request timed out"
        }
    except requests.RequestException as e:
        return {
            "success": False,
            "source": "gmail",
            "error": str(e)
        }


# =============================================================================
# JOB SEARCH (BACKUP) - Scrape Levels.fyi or company pages
# =============================================================================

@tool
def tinyfish_search_jobs(
    skills: List[str],
    experience_level: str,
    job_count: int = 2
) -> dict:
    """
    Search for jobs using TinyFish browser automation.
    Scrapes Levels.fyi (engineer-friendly job board) or company career pages.
    
    Args:
        skills: List of candidate's top skills
        experience_level: "entry", "mid", "senior"
        job_count: Number of jobs to find
        
    Returns:
        Dictionary with matched jobs
    """
    skills_str = ", ".join(skills[:5])
    
    # Use Levels.fyi - a tech-focused, scraper-friendly job board
    goal = f"""
    Find {job_count} Software Engineer jobs on this page.
    
    Look for positions suitable for a {experience_level} level candidate.
    Skills to match: {skills_str}
    
    For each job listing, extract:
    - Company name
    - Job title  
    - Location (city or Remote)
    - Salary/compensation if shown
    - Application URL or job link
    
    Focus on well-known tech companies.
    """
    
    # Levels.fyi is tech-focused and scraper-friendly
    url = "https://www.levels.fyi/jobs?searchText=software+engineer&countryId=254"
    
    print(f"[TinyFish] Searching Levels.fyi for {job_count} jobs...")
    
    try:
        response = requests.post(
            f"{TINYFISH_BASE_URL}/v1/automation/run",
            headers={
                "X-API-Key": TINYFISH_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "url": url,
                "goal": goal,
                "browser_profile": "lite"
            },
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        
        print(f"[TinyFish] Job search status: {result.get('status')}")
        
        if result.get("status") == "COMPLETED" and result.get("result"):
            return {
                "success": True,
                "source": "levels_fyi",
                "run_id": result.get("run_id"),
                "result": result.get("result"),
                "num_steps": result.get("num_of_steps", 0)
            }
        else:
            return {
                "success": False,
                "source": "levels_fyi",
                "run_id": result.get("run_id"),
                "error": result.get("error") or "No results returned",
                "status": result.get("status")
            }
        
    except requests.RequestException as e:
        print(f"[TinyFish] Job search error: {e}")
        return {
            "success": False,
            "source": "levels_fyi",
            "error": str(e)
        }


# =============================================================================
# SSE STREAMING - For live demo visualization
# =============================================================================

async def tinyfish_leetcode_stream(username: str) -> AsyncGenerator[str, None]:
    """
    Verify LeetCode with SSE streaming - yields events as they happen.
    Use for live demo to show browser automation progress.
    """
    import aiohttp
    import asyncio
    
    goal = f"""
    Navigate to LeetCode profile for '{username}'.
    Extract problems solved and recent activity.
    """
    
    yield json.dumps({
        "type": "start",
        "message": f"Starting LeetCode verification for {username}...",
        "username": username
    })
    
    yield json.dumps({
        "type": "step",
        "message": f"Navigating to leetcode.com/u/{username}/",
        "step": 1
    })
    
    await asyncio.sleep(1)
    
    try:
        async with aiohttp.ClientSession() as session:
            yield json.dumps({
                "type": "step", 
                "message": "Browser launched, loading profile page...",
                "step": 2
            })
            
            async with session.post(
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
                timeout=aiohttp.ClientTimeout(total=180)
            ) as response:
                
                yield json.dumps({
                    "type": "step",
                    "message": "Extracting profile data...",
                    "step": 3
                })
                
                result = await response.json()
                
                yield json.dumps({
                    "type": "complete",
                    "success": result.get("status") == "COMPLETED",
                    "result": result.get("result"),
                    "num_steps": result.get("num_of_steps", 0),
                    "run_id": result.get("run_id")
                })
                
    except Exception as e:
        yield json.dumps({
            "type": "error",
            "error": str(e)
        })


async def tinyfish_gmail_stream() -> AsyncGenerator[str, None]:
    """
    Check Gmail with SSE streaming for live demo.
    """
    import aiohttp
    import asyncio
    
    yield json.dumps({
        "type": "start",
        "message": "Starting Gmail verification..."
    })
    
    yield json.dumps({
        "type": "step",
        "message": "Opening Gmail sent folder...",
        "step": 1
    })
    
    await asyncio.sleep(1)
    
    try:
        async with aiohttp.ClientSession() as session:
            yield json.dumps({
                "type": "step",
                "message": "Scanning for job application emails...",
                "step": 2
            })
            
            async with session.post(
                f"{TINYFISH_BASE_URL}/v1/automation/run",
                headers={
                    "X-API-Key": TINYFISH_API_KEY,
                    "Content-Type": "application/json"
                },
                json={
                    "url": "https://mail.google.com/mail/u/0/#sent",
                    "goal": "Check sent folder for job application emails in last 24 hours. Count them and list recipients.",
                    "browser_profile": "stealth"
                },
                timeout=aiohttp.ClientTimeout(total=180)
            ) as response:
                
                yield json.dumps({
                    "type": "step",
                    "message": "Analyzing email contents...",
                    "step": 3
                })
                
                result = await response.json()
                
                yield json.dumps({
                    "type": "complete",
                    "success": result.get("status") == "COMPLETED",
                    "result": result.get("result"),
                    "num_steps": result.get("num_of_steps", 0)
                })
                
    except Exception as e:
        yield json.dumps({
            "type": "error",
            "error": str(e)
        })
