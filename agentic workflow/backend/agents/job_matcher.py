"""
Job Matcher Agent
Finds jobs matching the candidate's profile using:
- Yutori Browsing API (primary - Indeed)
- TinyFish (backup)
- LLM-generated suggestions (fallback)
"""
import json
import sys
sys.path.append('..')

from llm_factory import get_agent_llm
from graph.state import AgentState
from tools.yutori_tools import yutori_search_jobs
from tools.tinyfish_tools import tinyfish_search_jobs, tinyfish_get_leetcode_problems
from config import JOB_SEARCH_ROLE


JOB_MATCHER_SYSTEM_PROMPT = """You are the Job Matcher Agent for Cerebro, an AI job preparation coach.

Your job is to find {role} positions that match the candidate's profile.

You have access to real job search tools that browse job boards and return actual listings.

When presenting jobs:
1. Explain WHY each job is a good match for their specific skills
2. Identify any skill gaps they'd need to address
3. Give practical advice on the application

Be encouraging and specific.
""".format(role=JOB_SEARCH_ROLE)


async def job_matcher_agent(state: AgentState) -> AgentState:
    """
    Job Matcher agent node - finds matching jobs using web search tools.
    
    API Priority:
    1. Yutori Browsing (Indeed) - structured output
    2. TinyFish (Indeed) - backup
    3. Smart suggestions (LLM) - fallback
    
    Also fetches LeetCode problems using TinyFish!
    
    Reads: parsed_resume, daily_targets, daily_plan
    Writes: matched_jobs, agent_thoughts
    """
    # Extract resume data
    resume = state.get("parsed_resume", {})
    inferred = resume.get("inferred", {})
    targets = state.get("daily_targets", {"applications": 2, "leetcode": 5})
    daily_plan = state.get("daily_plan", {})
    
    # Get top skills
    skills = resume.get("skills", [])
    top_skills = [s.get("name") for s in skills[:10] if s.get("name")]
    if not top_skills:
        top_skills = ["Python", "JavaScript", "Software Development"]
    
    # Prepare search parameters
    experience_level = inferred.get("experience_level", "mid")
    skills_to_develop = inferred.get("skills_to_develop", [])
    job_count = targets.get("applications", 2)
    
    # Record thought
    thought = f"Job Matcher Agent: Searching for {job_count} {JOB_SEARCH_ROLE} jobs matching skills: {', '.join(top_skills[:5])}..."
    state["agent_thoughts"].append(thought)
    state["current_agent"] = "job_matcher"
    
    print(f"\n[Job Matcher] Starting job search for {experience_level} level, skills: {top_skills[:5]}")
    
    jobs = []
    job_source = "none"
    
    # ==========================================================================
    # STEP 1: Try Yutori Browsing API (Indeed) - BEST OPTION
    # ==========================================================================
    try:
        print("[Job Matcher] 🔍 Trying Yutori Browsing on Indeed...")
        state["agent_thoughts"].append("Job Matcher Agent: Searching Indeed via Yutori Browsing API...")
        
        yutori_result = yutori_search_jobs.invoke({
            "skills": top_skills,
            "experience_level": experience_level,
            "job_count": job_count
        })
        
        print(f"[Job Matcher] Yutori result success: {yutori_result.get('success')}")
        
        if yutori_result.get("success"):
            yutori_jobs = yutori_result.get("jobs", [])
            if yutori_jobs and len(yutori_jobs) > 0:
                jobs = yutori_jobs
                job_source = "yutori_indeed"
                print(f"[Job Matcher] ✅ Found {len(jobs)} jobs from Yutori!")
                state["agent_thoughts"].append(f"Job Matcher Agent: ✅ Found {len(jobs)} jobs from Indeed via Yutori!")
                
    except Exception as e:
        print(f"[Job Matcher] Yutori exception: {e}")
        state["agent_thoughts"].append(f"Job Matcher Agent: Yutori search failed - {str(e)[:50]}")
    
    # ==========================================================================
    # STEP 2: Try TinyFish (backup)
    # ==========================================================================
    if not jobs:
        try:
            print("[Job Matcher] 🔍 Trying TinyFish search as backup...")
            state["agent_thoughts"].append("Job Matcher Agent: Trying TinyFish as backup...")
            
            tf_result = tinyfish_search_jobs.invoke({
                "skills": top_skills,
                "experience_level": experience_level,
                "job_count": job_count
            })
            
            print(f"[Job Matcher] TinyFish result success: {tf_result.get('success')}")
            
            if tf_result.get("success") and tf_result.get("result"):
                # Parse the result text
                parsed_jobs = _parse_job_results(tf_result["result"], job_count, top_skills, experience_level)
                if parsed_jobs:
                    jobs = parsed_jobs
                    job_source = "tinyfish"
                    print(f"[Job Matcher] ✅ Found {len(jobs)} jobs from TinyFish!")
                    state["agent_thoughts"].append(f"Job Matcher Agent: ✅ Found {len(jobs)} jobs via TinyFish!")
                    
        except Exception as e:
            print(f"[Job Matcher] TinyFish exception: {e}")
            state["agent_thoughts"].append(f"Job Matcher Agent: TinyFish search failed - {str(e)[:50]}")
    
    # ==========================================================================
    # STEP 3: Fallback to smart LLM-generated suggestions
    # ==========================================================================
    if not jobs:
        print("[Job Matcher] ⚠️ API searches failed, creating smart suggestions...")
        jobs = _create_smart_job_suggestions(resume, inferred, job_count)
        job_source = "llm_generated"
        state["agent_thoughts"].append(f"Job Matcher Agent: Generated {len(jobs)} personalized job suggestions based on profile.")
    
    # ==========================================================================
    # FORMAT JOBS with match reasoning
    # ==========================================================================
    formatted_jobs = []
    for job in jobs:
        formatted_job = {
            "company": job.get("company", "Company"),
            "title": job.get("title", JOB_SEARCH_ROLE),
            "location": job.get("location", "Remote"),
            "salary_range": job.get("salary_range"),
            "apply_url": job.get("apply_url"),
            "description": job.get("description", ""),
            "match_reason": job.get("match_reason") or _generate_match_reason(job, top_skills, experience_level),
            "skill_gaps": job.get("skill_gaps") or skills_to_develop[:3],
            "source": job_source
        }
        formatted_jobs.append(formatted_job)
    
    # ==========================================================================
    # Update state
    # ==========================================================================
    state["matched_jobs"] = formatted_jobs
    state["agent_thoughts"].append(f"Job Matcher Agent: Completed with {len(formatted_jobs)} matching jobs (source: {job_source}).")
    state["stream_events"].append({
        "type": "agent_complete",
        "agent": "job_matcher",
        "output": {"jobs": formatted_jobs, "source": job_source}
    })
    
    print(f"[Job Matcher] ✅ Complete - {len(formatted_jobs)} jobs from {job_source}\n")
    
    return state


def _parse_job_results(result_text: str, count: int, skills: list, level: str) -> list:
    """
    Parse unstructured job search results into structured format.
    """
    jobs = []
    
    if not result_text:
        return jobs
    
    # Try to extract job info from text
    lines = result_text.split('\n')
    current_job = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_job.get("company") or current_job.get("title"):
                jobs.append(current_job)
                current_job = {}
            continue
            
        lower = line.lower()
        if "company" in lower or "@" in line:
            current_job["company"] = line.split(":")[-1].strip() if ":" in line else line
        elif "title" in lower or "position" in lower or "engineer" in lower:
            current_job["title"] = line.split(":")[-1].strip() if ":" in line else line
        elif "location" in lower or "remote" in lower:
            current_job["location"] = line.split(":")[-1].strip() if ":" in line else line
        elif "$" in line or "salary" in lower:
            current_job["salary_range"] = line.split(":")[-1].strip() if ":" in line else line
        elif "http" in lower:
            current_job["apply_url"] = line
    
    # Add last job if exists
    if current_job.get("company") or current_job.get("title"):
        jobs.append(current_job)
    
    return jobs[:count]


def _generate_match_reason(job: dict, skills: list, level: str) -> str:
    """Generate a match reason based on job and candidate info."""
    company = job.get("company", "this company")
    title = job.get("title", "this role")
    skill_str = ", ".join(skills[:3]) if skills else "your technical skills"
    
    return f"Your expertise in {skill_str} aligns well with {title} at {company}. This {level}-level position matches your experience."


def _create_smart_job_suggestions(resume: dict, inferred: dict, count: int) -> list:
    """
    Create intelligent job suggestions based on candidate's profile.
    Used when API calls fail - still provides personalized results.
    """
    skills = resume.get("skills", [])
    top_skills = [s.get("name", "") for s in skills[:5]]
    experience_level = inferred.get("experience_level", "mid")
    skills_to_develop = inferred.get("skills_to_develop", [])
    
    salary_map = {
        "entry": "$80,000 - $120,000",
        "junior": "$80,000 - $120,000",
        "mid": "$120,000 - $160,000", 
        "senior": "$160,000 - $220,000",
        "lead": "$200,000 - $280,000"
    }
    
    company_profiles = [
        {
            "company": "Stripe",
            "description": "Payment infrastructure for the internet",
            "why": "Known for excellent engineering culture and challenging problems"
        },
        {
            "company": "Databricks",
            "description": "Unified analytics platform",
            "why": "Great for data-focused engineers with growth potential"
        },
        {
            "company": "Figma",
            "description": "Collaborative design platform",
            "why": "Innovative product with strong engineering team"
        },
        {
            "company": "Vercel",
            "description": "Frontend cloud platform",
            "why": "If you love modern web development"
        },
        {
            "company": "Linear",
            "description": "Modern issue tracking",
            "why": "Small team, high impact, beautiful products"
        },
        {
            "company": "Scale AI",
            "description": "AI data infrastructure",
            "why": "At the forefront of AI/ML infrastructure"
        }
    ]
    
    jobs = []
    skills_str = ", ".join(top_skills[:3]) if top_skills else "software development"
    
    for i in range(min(count, len(company_profiles))):
        profile = company_profiles[i]
        jobs.append({
            "company": profile["company"],
            "title": JOB_SEARCH_ROLE,
            "location": "Remote / San Francisco",
            "salary_range": salary_map.get(experience_level, "$120,000 - $160,000"),
            "apply_url": f"https://jobs.lever.co/{profile['company'].lower()}",
            "description": profile["description"],
            "match_reason": f"Your skills in {skills_str} are a great fit. {profile['why']}",
            "skill_gaps": skills_to_develop[:2] if skills_to_develop else ["System Design"]
        })
    
    return jobs
