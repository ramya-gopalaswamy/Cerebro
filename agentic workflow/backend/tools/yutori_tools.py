"""
Yutori API Tools
- Browsing: One-time web scraping with structured output
- Scouting: Recurring job monitoring (background)
"""
import requests
import time
from typing import List, Optional
from langchain_core.tools import tool
import sys
sys.path.append('..')

from config import YUTORI_API_KEY, YUTORI_BASE_URL, JOB_SEARCH_ROLE


# =============================================================================
# JSON SCHEMAS FOR STRUCTURED OUTPUT
# =============================================================================

JOB_OUTPUT_SCHEMA = {
    "type": "json",
    "json_schema": {
        "type": "object",
        "properties": {
            "jobs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "company": {"type": "string", "description": "Company name"},
                        "title": {"type": "string", "description": "Job title"},
                        "location": {"type": "string", "description": "Job location"},
                        "salary_range": {"type": "string", "description": "Salary if shown"},
                        "apply_url": {"type": "string", "description": "Application URL"},
                        "description": {"type": "string", "description": "Brief description"}
                    },
                    "required": ["company", "title"]
                }
            }
        },
        "required": ["jobs"]
    }
}


COMPANY_RESEARCH_SCHEMA = {
    "type": "json",
    "json_schema": {
        "type": "object",
        "properties": {
            "company_name": {"type": "string"},
            "what_they_do": {"type": "string"},
            "tech_stack": {"type": "array", "items": {"type": "string"}},
            "company_size": {"type": "string"},
            "interview_process": {"type": "string"},
            "culture": {"type": "string"},
            "recent_news": {"type": "string"}
        },
        "required": ["company_name", "what_they_do"]
    }
}


# =============================================================================
# YUTORI BROWSING API - One-time web scraping
# =============================================================================

def yutori_browse(task: str, start_url: str, output_schema: dict = None, max_wait: int = 120) -> dict:
    """
    Execute a Yutori Browsing task with polling.
    Returns view_url immediately for live viewing!
    
    Args:
        task: Natural language task description
        start_url: URL to start browsing from
        output_schema: Optional JSON schema for structured output
        max_wait: Maximum seconds to wait
        
    Returns:
        Result with view_url, structured_result, etc.
    """
    headers = {
        "X-API-Key": YUTORI_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "task": task,
        "start_url": start_url,
        "max_steps": 50
    }
    
    if output_schema:
        payload["task_spec"] = {"output_schema": output_schema}
    
    try:
        print(f"[Yutori Browsing] Creating task...")
        print(f"[Yutori Browsing] URL: {start_url}")
        
        response = requests.post(
            f"{YUTORI_BASE_URL}/v1/browsing/tasks",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        task_id = result.get("task_id")
        view_url = result.get("view_url")
        status = result.get("status")
        
        print(f"[Yutori Browsing] Task ID: {task_id}")
        print(f"[Yutori Browsing] View URL: {view_url}")
        print(f"[Yutori Browsing] Status: {status}")
        
        # If already succeeded
        if status == "succeeded":
            return {
                "success": True,
                "task_id": task_id,
                "view_url": view_url,
                "result": result.get("result"),
                "structured_result": result.get("structured_result")
            }
        
        # Poll for completion
        poll_url = f"{YUTORI_BASE_URL}/v1/browsing/tasks/{task_id}"
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            time.sleep(5)  # Poll every 5 seconds
            
            try:
                poll_response = requests.get(poll_url, headers=headers, timeout=10)
                poll_response.raise_for_status()
                poll_result = poll_response.json()
                
                status = poll_result.get("status")
                print(f"[Yutori Browsing] Status: {status}")
                
                if status == "succeeded":
                    return {
                        "success": True,
                        "task_id": task_id,
                        "view_url": view_url,
                        "result": poll_result.get("result"),
                        "structured_result": poll_result.get("structured_result")
                    }
                elif status == "failed":
                    return {
                        "success": False,
                        "task_id": task_id,
                        "view_url": view_url,
                        "error": poll_result.get("result", "Task failed")
                    }
                    
            except Exception as poll_error:
                print(f"[Yutori Browsing] Poll error: {poll_error}")
                continue
        
        return {
            "success": False,
            "task_id": task_id,
            "view_url": view_url,
            "error": f"Task timed out after {max_wait}s",
            "partial_result": result.get("result")
        }
        
    except requests.RequestException as e:
        print(f"[Yutori Browsing] Error: {e}")
        return {"success": False, "error": str(e)}


# =============================================================================
# FAANG CAREER PAGES - Direct company website scraping (most reliable!)
# =============================================================================

FAANG_CAREER_PAGES = [
    {
        "company": "Google",
        "url": "https://www.google.com/about/careers/applications/jobs/results/?q=software%20engineer",
        "friendly": True
    },
    {
        "company": "Meta",
        "url": "https://www.metacareers.com/jobs?q=software%20engineer",
        "friendly": True
    },
    {
        "company": "Amazon",
        "url": "https://www.amazon.jobs/en/search?base_query=software+engineer",
        "friendly": True
    },
    {
        "company": "Microsoft",
        "url": "https://careers.microsoft.com/us/en/search-results?keywords=software%20engineer",
        "friendly": True
    },
    {
        "company": "Apple",
        "url": "https://jobs.apple.com/en-us/search?search=software%20engineer&sort=relevance",
        "friendly": True
    },
    {
        "company": "Netflix",
        "url": "https://jobs.netflix.com/search?q=software%20engineer",
        "friendly": True
    }
]


@tool
def yutori_search_jobs(
    skills: List[str],
    experience_level: str,
    job_count: int = 3
) -> dict:
    """
    Search for Software Engineer jobs by scraping FAANG company career pages.
    Uses Yutori Browsing API to extract jobs directly from company websites.
    
    Args:
        skills: Candidate's top skills
        experience_level: "entry", "mid", "senior"
        job_count: Number of jobs to find
        
    Returns:
        Structured job listings from company career pages
    """
    skills_str = ", ".join(skills[:5])
    all_jobs = []
    
    # Select companies to search (rotate through FAANG)
    companies_to_search = FAANG_CAREER_PAGES[:min(job_count, len(FAANG_CAREER_PAGES))]
    
    print(f"[Yutori] Searching FAANG career pages for {JOB_SEARCH_ROLE} jobs...")
    
    for company_info in companies_to_search:
        company = company_info["company"]
        url = company_info["url"]
        
        task = f"""
        Find 1-2 {JOB_SEARCH_ROLE} jobs on this {company} careers page.
        
        Look for positions suitable for {experience_level} level.
        Preferred skills: {skills_str}
        
        For each job listing, extract:
        1. Job title (exact title from page)
        2. Location (city or Remote)
        3. Job ID or requisition number if visible
        4. Brief description or requirements summary
        5. The direct apply/job detail URL
        
        Return the most relevant positions for a software engineer.
        """
        
        print(f"[Yutori] 🔍 Searching {company} careers...")
        
        result = yutori_browse(
            task=task,
            start_url=url,
            output_schema=JOB_OUTPUT_SCHEMA,
            max_wait=60  # Shorter wait per company
        )
        
        if result.get("success"):
            if result.get("structured_result"):
                jobs = result["structured_result"].get("jobs", [])
                for job in jobs:
                    job["company"] = company
                    job["source"] = f"{company.lower()}_careers"
                all_jobs.extend(jobs)
                print(f"[Yutori] ✅ Found {len(jobs)} jobs from {company}")
            elif result.get("result"):
                # Parse from raw text result
                raw_job = {
                    "company": company,
                    "title": JOB_SEARCH_ROLE,
                    "location": "Multiple Locations",
                    "description": result.get("result", "")[:200],
                    "apply_url": url,
                    "source": f"{company.lower()}_careers"
                }
                all_jobs.append(raw_job)
                print(f"[Yutori] ✅ Got raw result from {company}")
        else:
            print(f"[Yutori] ⚠️ {company} search returned no results")
        
        # Stop if we have enough jobs
        if len(all_jobs) >= job_count:
            break
    
    if all_jobs:
        return {
            "success": True,
            "jobs": all_jobs[:job_count],
            "source": "faang_careers",
            "companies_searched": [c["company"] for c in companies_to_search]
        }
    else:
        return {
            "success": False,
            "jobs": [],
            "error": "No jobs found from FAANG career pages"
        }


# =============================================================================
# COMPANY RESEARCH - For War Room feature
# =============================================================================

@tool
def yutori_research_company(company_name: str) -> dict:
    """
    Research a company for interview preparation using Yutori Browsing.
    
    Args:
        company_name: Name of the company to research
        
    Returns:
        Structured company research including tech stack, culture, interview tips
    """
    task = f"""
    Research {company_name} for a Software Engineer interview:
    
    Find and extract:
    1. What the company does (main product/service)
    2. Their tech stack and technologies used
    3. Company size and stage (startup, mid-size, enterprise)
    4. Engineering culture and values
    5. Typical interview process
    6. Recent news (funding, launches, etc.)
    
    Focus on information useful for interview preparation.
    """
    
    print(f"[Yutori] Researching {company_name}...")
    
    result = yutori_browse(
        task=task,
        start_url=f"https://www.google.com/search?q={company_name}+engineering+culture+interview",
        output_schema=COMPANY_RESEARCH_SCHEMA,
        max_wait=60
    )
    
    if result.get("success"):
        return {
            "success": True,
            "company": company_name,
            "research": result.get("structured_result") or result.get("result"),
            "view_url": result.get("view_url")
        }
    else:
        return {
            "success": False,
            "company": company_name,
            "error": result.get("error"),
            "view_url": result.get("view_url")
        }


# =============================================================================
# YUTORI SCOUTING API - Recurring job monitoring
# =============================================================================

@tool
def yutori_create_job_scout(
    skills: List[str],
    experience_level: str,
    location: Optional[str] = None
) -> dict:
    """
    Create a Yutori Scout for recurring job monitoring.
    This runs in the background and can send webhooks when new jobs are found.
    
    Args:
        skills: Candidate skills to match
        experience_level: Experience level
        location: Preferred location
        
    Returns:
        Scout ID and details
    """
    skills_str = ", ".join(skills[:10])
    location_str = f" in {location}" if location else " in United States"
    
    query = f"""
    Monitor for new {JOB_SEARCH_ROLE} job postings{location_str} for a {experience_level} level candidate.
    
    Required skills: {skills_str}
    
    Alert when relevant new positions are posted on major job boards.
    """
    
    try:
        print(f"[Yutori Scout] Creating job monitor...")
        
        response = requests.post(
            f"{YUTORI_BASE_URL}/v1/scouting/tasks",
            headers={
                "X-API-Key": YUTORI_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "query": query,
                "output_interval": 86400,  # Daily check
                "skip_email": True,
                "task_spec": {
                    "output_schema": JOB_OUTPUT_SCHEMA
                }
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        print(f"[Yutori Scout] Created scout: {result.get('id')}")
        
        return {
            "success": True,
            "scout_id": result.get("id"),
            "display_name": result.get("display_name"),
            "next_run": result.get("next_run_timestamp"),
            "status": "created"
        }
        
    except requests.RequestException as e:
        print(f"[Yutori Scout] Error: {e}")
        return {"success": False, "error": str(e)}


# =============================================================================
# HELPER: Get task status (for async operations)
# =============================================================================

def yutori_get_task_status(task_id: str) -> dict:
    """Get current status of a Yutori browsing task."""
    try:
        response = requests.get(
            f"{YUTORI_BASE_URL}/v1/browsing/tasks/{task_id}",
            headers={"X-API-Key": YUTORI_API_KEY},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
