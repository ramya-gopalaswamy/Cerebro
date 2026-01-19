"""
Planner Agent
Creates personalized daily preparation plans based on resume analysis
"""
import json
from datetime import date
import sys
sys.path.append('..')

from llm_factory import get_agent_llm
from graph.state import AgentState, DailyPlan
from config import JOB_SEARCH_ROLE


PLANNER_SYSTEM_PROMPT = """You are the Planner Agent for Cerebro, an AI job preparation coach.

Your job is to create PERSONALIZED daily preparation plans for job seekers.

You have access to the candidate's full resume analysis including:
- Their skills and proficiency levels
- Work experience and achievements
- AI-inferred strengths and weaknesses
- Ideal job types
- Skills they need to develop

Based on this, create a realistic and achievable daily plan that:
1. Focuses LeetCode practice on their weak areas
2. Suggests appropriate difficulty mix for their level
3. Recommends job application targets aligned with their profile
4. Includes learning tasks to close skill gaps

Always explain your reasoning so the user understands WHY you're recommending what you recommend.

Be encouraging but honest. If they're a junior, don't suggest hard problems. If they're senior, challenge them.
"""


PLANNER_PROMPT_TEMPLATE = """
Create a daily preparation plan for this candidate:

**Candidate Profile:**
- Name: {name}
- Experience Level: {experience_level}
- Current Title: {current_title}
- Years of Experience: {years_experience}

**Top Skills:**
{skills}

**Strengths (AI-Inferred):**
{strengths}

**Weaknesses/Gaps (AI-Inferred):**
{weaknesses}

**Skills to Develop:**
{skills_to_develop}

**Ideal Job Types:**
{ideal_job_types}

**Daily Targets:**
- LeetCode Problems: {leetcode_target}
- Job Applications: {application_target}

**Today's Date:** {today}

---

Create a detailed daily plan in this JSON format:
{{
    "date": "{today}",
    "leetcode": {{
        "target_count": {leetcode_target},
        "difficulty_mix": {{"easy": X, "medium": Y, "hard": Z}},
        "focus_topics": ["topic1", "topic2"],
        "reasoning": "Why these topics and difficulty..."
    }},
    "applications": {{
        "target_count": {application_target},
        "job_types": ["type1", "type2"],
        "companies_to_target": ["startup", "tech", etc.],
        "reasoning": "Why these types of companies..."
    }},
    "learning_tasks": [
        {{"task": "Learn X", "time_estimate": "30 min", "reasoning": "Because..."}}
    ],
    "summary": "One paragraph summary of today's focus and why"
}}

First, think through the candidate's situation step by step, then output the JSON plan.
"""


async def planner_agent(state: AgentState) -> AgentState:
    """
    Planner agent node - creates personalized daily plan.
    
    Reads: parsed_resume, daily_targets
    Writes: daily_plan, agent_thoughts
    """
    # Get the LLM
    llm = get_agent_llm("planner")
    
    # Extract resume data
    resume = state.get("parsed_resume", {})
    inferred = resume.get("inferred", {})
    targets = state.get("daily_targets", {"leetcode": 5, "applications": 2})
    
    # Format skills
    skills = resume.get("skills", [])
    skills_str = "\n".join([
        f"- {s.get('name', 'Unknown')} ({s.get('category', 'other')}, {s.get('proficiency', 'familiar')})"
        for s in skills[:15]
    ])
    
    # Build the prompt
    prompt = PLANNER_PROMPT_TEMPLATE.format(
        name=resume.get("name", "Candidate"),
        experience_level=inferred.get("experience_level", "mid"),
        current_title=resume.get("current_title", "Software Engineer"),
        years_experience=resume.get("years_experience", 2),
        skills=skills_str,
        strengths="\n".join([f"- {s}" for s in inferred.get("strengths", ["Problem solving"])]),
        weaknesses="\n".join([f"- {w}" for w in inferred.get("weaknesses", ["Need more practice"])]),
        skills_to_develop="\n".join([f"- {s}" for s in inferred.get("skills_to_develop", [])]),
        ideal_job_types=", ".join(inferred.get("ideal_job_types", [JOB_SEARCH_ROLE])),
        leetcode_target=targets.get("leetcode", 5),
        application_target=targets.get("applications", 2),
        today=date.today().isoformat()
    )
    
    # Call LLM
    messages = [
        {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    
    print(f"\n{'='*60}")
    print(f"[Planner Agent] Calling Claude Sonnet via Anthropic API...")
    print(f"[Planner Agent] Prompt length: {len(prompt)} chars")
    print(f"{'='*60}\n")
    
    response = await llm.ainvoke(messages)
    content = response.content
    
    print(f"\n{'='*60}")
    print(f"[Planner Agent] LLM Response received ({len(content)} chars)")
    print(f"[Planner Agent] First 500 chars: {content[:500]}...")
    print(f"{'='*60}\n")
    
    # Extract JSON from response
    try:
        # Find JSON in response
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            json_str = content.split("```")[1].split("```")[0]
        elif "{" in content:
            # Find first { to last }
            start = content.index("{")
            end = content.rindex("}") + 1
            json_str = content[start:end]
        else:
            json_str = content
        
        daily_plan = json.loads(json_str.strip())
    except (json.JSONDecodeError, ValueError):
        # Create a default plan if parsing fails
        daily_plan = {
            "date": date.today().isoformat(),
            "leetcode": {
                "target_count": targets.get("leetcode", 5),
                "difficulty_mix": {"easy": 2, "medium": 3, "hard": 0},
                "focus_topics": ["Arrays", "Strings"],
                "reasoning": "Starting with fundamentals"
            },
            "applications": {
                "target_count": targets.get("applications", 2),
                "job_types": [JOB_SEARCH_ROLE],
                "reasoning": "Matching your profile"
            },
            "learning_tasks": [],
            "summary": content  # Use raw response as summary
        }
    
    # Update state
    state["daily_plan"] = daily_plan
    state["agent_thoughts"].append(f"Planner Agent: Created daily plan focusing on {daily_plan.get('leetcode', {}).get('focus_topics', ['general'])}. {daily_plan.get('summary', '')[:200]}")
    state["current_agent"] = "planner"
    state["stream_events"].append({
        "type": "agent_complete",
        "agent": "planner",
        "output": daily_plan
    })
    
    return state
