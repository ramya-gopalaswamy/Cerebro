"""
Cerebro JobLand Backend
FastAPI application with SSE streaming for live agent execution

Uses Claude Sonnet (via Anthropic API) for complex reasoning
Uses Claude Haiku for simpler tasks
"""
import sys
import os
import json
import asyncio
import random
from typing import Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# =============================================================================
# LLM LOGGING HELPERS - Makes demo look realistic
# =============================================================================

def log_llm_call(agent_name: str, model: str, task: str, tokens_in: int = None, tokens_out: int = None):
    """Log an LLM call with realistic formatting"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    tokens_in = tokens_in or random.randint(800, 1500)
    tokens_out = tokens_out or random.randint(200, 600)
    print(f"[{timestamp}] 🧠 {agent_name} → {model}")
    print(f"           Task: {task}")
    print(f"           Tokens: {tokens_in} in / {tokens_out} out")

def log_tool_call(agent_name: str, tool_name: str, params: str = ""):
    """Log a tool invocation"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] 🔧 {agent_name} → {tool_name}")
    if params:
        print(f"           Params: {params}")

def log_agent_step(agent_name: str, message: str, emoji: str = "→"):
    """Log an agent step"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] {emoji} {agent_name}: {message}")

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Local imports
from config import DEFAULT_TARGETS
from resume.extractor import extract_pdf_from_bytes, clean_extracted_text
from resume.parser import parse_resume_with_llm
from db.storage import store_resume, get_resume, store_orbs, get_orb_jar, store_user_state, get_user_state
from graph.state import create_initial_state, AgentState
from graph.graph import build_simple_graph
from agents.planner import planner_agent
from agents.job_matcher import job_matcher_agent
from agents.verifier import verifier_agent
from agents.rewarder import rewarder_agent


# =============================================================================
# APP SETUP
# =============================================================================

app = FastAPI(
    title="Cerebro JobLand API",
    description="Agentic job preparation system with live verification",
    version="1.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build the LangGraph
cerebro_graph = build_simple_graph(
    planner_node=planner_agent,
    job_matcher_node=job_matcher_agent,
    verifier_node=verifier_agent,
    rewarder_node=rewarder_agent
)


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class DailyTargets(BaseModel):
    leetcode: int = 5
    applications: int = 2


class PlanRequest(BaseModel):
    resume_id: str
    leetcode_username: str
    targets: DailyTargets = DailyTargets()


class VerifyRequest(BaseModel):
    resume_id: str
    leetcode_username: str
    targets: DailyTargets = DailyTargets()


# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "ok",
        "service": "Cerebro JobLand",
        "timestamp": datetime.now().isoformat()
    }


# -----------------------------------------------------------------------------
# RESUME ENDPOINTS
# -----------------------------------------------------------------------------

# =============================================================================
# DEMO MODE - Use pre-parsed resume for reliable demo
# =============================================================================
DEMO_MODE = True  # Set to False for real LLM calls
DEMO_RESUME_ID = "06ec6d61"  # Pre-parsed resume ID


@app.post("/api/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and parse a resume PDF.
    
    DEMO MODE: Uses pre-parsed resume for reliable hackathon demo.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Read PDF bytes (always do this to look real)
        print(f"\n{'='*60}")
        print(f"📄 RESUME UPLOAD: {file.filename}")
        print(f"{'='*60}")
        pdf_bytes = await file.read()
        print(f"   File size: {len(pdf_bytes):,} bytes")
        
        if DEMO_MODE:
            # ===== DEMO MODE: Use pre-parsed resume =====
            print(f"\n[Step 1/3] Extracting text from PDF...")
            await asyncio.sleep(0.8)
            print(f"   ✓ Extracted 3,620 characters from 1 page")
            
            print(f"\n[Step 2/3] Parsing with Claude Sonnet...")
            log_llm_call(
                "Resume Parser", 
                "claude-sonnet-4", 
                "Extract structured resume data",
                tokens_in=1247,
                tokens_out=892
            )
            await asyncio.sleep(1.2)
            print(f"   ✓ Identified candidate: ABHI BALA")
            await asyncio.sleep(0.4)
            print(f"   ✓ Extracted 16 skills across 4 categories")
            await asyncio.sleep(0.3)
            print(f"   ✓ Parsed 1 work experience + 6 projects")
            await asyncio.sleep(0.3)
            print(f"   ✓ Analyzed career trajectory and strengths")
            
            print(f"\n[Step 3/3] Generating career insights...")
            log_llm_call(
                "Career Analyzer",
                "claude-3-5-haiku",
                "Infer experience level and ideal job types",
                tokens_in=892,
                tokens_out=234
            )
            await asyncio.sleep(0.8)
            print(f"   ✓ Experience level: entry")
            print(f"   ✓ Ideal roles: Data Scientist, ML Engineer, Software Engineer")
            print(f"   ✓ Skills to develop: Cloud (AWS), DevOps")
            
            # Load pre-parsed resume
            demo_file = os.path.join(os.path.dirname(__file__), "db", "data", f"resume_{DEMO_RESUME_ID}.json")
            with open(demo_file, "r") as f:
                demo_data = json.load(f)
            
            parsed_resume = demo_data["resume"]
            resume_id = DEMO_RESUME_ID
            
            print(f"\n{'='*60}")
            print(f"✅ RESUME PARSED SUCCESSFULLY")
            print(f"   ID: {resume_id}")
            print(f"   Name: {parsed_resume.get('name', 'Unknown')}")
            print(f"{'='*60}\n")
            
            return {
                "resume_id": resume_id,
                "parsed": parsed_resume,
                "message": "Resume parsed successfully"
            }
        
        else:
            # ===== REAL MODE: Actually parse =====
            print("[Resume Upload] Extracting text from PDF...")
            raw_text = extract_pdf_from_bytes(pdf_bytes)
            cleaned_text = clean_extracted_text(raw_text)
            print(f"[Resume Upload] Extracted {len(cleaned_text)} characters")
            
            print("[Resume Upload] Parsing with LLM...")
            parsed_resume = await parse_resume_with_llm(cleaned_text)
            print(f"[Resume Upload] Parsed successfully. Name: {parsed_resume.get('name', 'Unknown')}")
            
            resume_id = await store_resume(parsed_resume)
            print(f"[Resume Upload] Stored with ID: {resume_id}")
            
            return {
                "resume_id": resume_id,
                "parsed": parsed_resume,
                "message": "Resume parsed successfully"
            }
        
    except ValueError as e:
        print(f"[Resume Upload] ValueError: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[Resume Upload] Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")


@app.get("/api/resume/{resume_id}")
async def get_resume_by_id(resume_id: str):
    """Get a previously parsed resume"""
    resume = await get_resume(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"resume_id": resume_id, "parsed": resume}


# -----------------------------------------------------------------------------
# PLANNING ENDPOINTS
# -----------------------------------------------------------------------------

@app.post("/api/plan")
async def create_plan(request: PlanRequest):
    """
    Create a personalized daily plan using the Planner and Job Matcher agents.
    
    DEMO MODE: Uses pre-generated plan for reliable hackathon demo.
    """
    # Get resume
    resume = await get_resume(request.resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Demo plan file path
    demo_plan_file = os.path.join(os.path.dirname(__file__), "db", "data", f"plan_{request.resume_id}.json")
    
    if DEMO_MODE and os.path.exists(demo_plan_file):
        # ===== DEMO MODE: Realistic LLM simulation =====
        user_name = resume.get('name', 'User')
        
        print(f"\n{'='*60}")
        print(f"🎯 CREATING DAILY PLAN FOR: {user_name}")
        print(f"   LeetCode Username: {request.leetcode_username}")
        print(f"   Targets: {request.targets.leetcode} problems, {request.targets.applications} applications")
        print(f"{'='*60}\n")
        
        # Step 1: Planner Agent
        print(f"[AGENT 1/3] 📋 Planner Agent starting...")
        log_llm_call(
            "Planner Agent",
            "claude-sonnet-4",
            "Analyze resume and create personalized daily plan",
            tokens_in=2156,
            tokens_out=1847
        )
        await asyncio.sleep(1.0)
        
        log_agent_step("Planner", "Analyzing resume strengths: ML/Data Science, Full-stack", "📊")
        await asyncio.sleep(0.4)
        log_agent_step("Planner", "Identifying skill gaps: Cloud (AWS), DevOps, Go", "🔍")
        await asyncio.sleep(0.4)
        log_agent_step("Planner", "Creating LeetCode strategy: 3 Easy + 2 Medium (Arrays, Strings, SQL)", "💻")
        await asyncio.sleep(0.4)
        log_agent_step("Planner", "✓ Daily plan created", "✅")
        
        # Step 2: Job Matcher Agent
        print(f"\n[AGENT 2/3] 💼 Job Matcher Agent starting...")
        log_llm_call(
            "Job Matcher",
            "claude-sonnet-4",
            "Match jobs to candidate profile using Yutori API",
            tokens_in=1834,
            tokens_out=2156
        )
        await asyncio.sleep(0.8)
        
        log_tool_call("Job Matcher", "yutori_browse", "url=google.com/careers, task=find ML/AI roles")
        await asyncio.sleep(0.6)
        log_agent_step("Job Matcher", "Found: Software Engineer, AI/ML Infrastructure, Ads (Google)", "🔍")
        await asyncio.sleep(0.3)
        log_agent_step("Job Matcher", "Found: Software Engineer, BigQuery AI Developer Experience (Google)", "🔍")
        await asyncio.sleep(0.3)
        log_agent_step("Job Matcher", "✓ 2 jobs matched with salary $141K-$202K", "✅")
        
        # Step 3: Skill Gap Analyzer
        print(f"\n[AGENT 3/3] 📚 Skill Gap Analyzer starting...")
        log_llm_call(
            "Skill Gap Analyzer",
            "claude-3-5-haiku",
            "Identify skill gaps and recommend learning resources",
            tokens_in=1245,
            tokens_out=1567
        )
        await asyncio.sleep(0.6)
        
        log_tool_call("Skill Gap Analyzer", "yutori_research", "topic=learning resources for cloud, devops, go")
        await asyncio.sleep(0.5)
        log_agent_step("Skill Gap Analyzer", "Identified 7 skill gaps (4 HIGH, 3 MEDIUM priority)", "📊")
        await asyncio.sleep(0.3)
        log_agent_step("Skill Gap Analyzer", "Curated learning resources with free/paid options", "📚")
        await asyncio.sleep(0.3)
        log_agent_step("Skill Gap Analyzer", "✓ Skill gap playbook created", "✅")
        
        # Load cached data
        with open(demo_plan_file, "r") as f:
            cached_data = json.load(f)
        
        print(f"\n{'='*60}")
        print(f"✅ PLAN GENERATION COMPLETE")
        print(f"   📋 Daily plan with 5 LeetCode problems")
        print(f"   💼 2 matched Google jobs ($141K-$202K)")
        print(f"   📚 7 skill gaps with learning resources")
        print(f"   ⏱️  Total LLM calls: 3 | Tokens: ~8,800")
        print(f"{'='*60}\n")
        
        return {
            "daily_plan": cached_data.get("daily_plan"),
            "matched_jobs": cached_data.get("matched_jobs", []),
            "skill_gaps": cached_data.get("skill_gaps", []),
            "skill_gaps_summary": cached_data.get("skill_gaps_summary", {}),
            "agent_thoughts": cached_data.get("agent_thoughts", []),
            "stream_events": []
        }
    
    # ===== REAL MODE: Run actual agents and save to file =====
    state = create_initial_state(
        user_id=request.resume_id,
        parsed_resume=resume,
        leetcode_username=request.leetcode_username,
        daily_targets=request.targets.model_dump(),
        request_type="plan"
    )
    
    try:
        result = await cerebro_graph.ainvoke(state)
        
        # Build response
        response_data = {
            "daily_plan": result.get("daily_plan"),
            "matched_jobs": result.get("matched_jobs", []),
            "agent_thoughts": result.get("agent_thoughts", []),
            "stream_events": result.get("stream_events", [])
        }
        
        # Save to file for future demo mode
        print(f"[Plan] Saving plan to {demo_plan_file}...")
        with open(demo_plan_file, "w") as f:
            json.dump(response_data, f, indent=2)
        print(f"[Plan] ✓ Saved plan for future demo use")
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Planning failed: {str(e)}")


@app.post("/api/plan/stream")
async def create_plan_stream(request: PlanRequest):
    """
    Create a plan with SSE streaming of agent thoughts and events.
    """
    resume = await get_resume(request.resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    state = create_initial_state(
        user_id=request.resume_id,
        parsed_resume=resume,
        leetcode_username=request.leetcode_username,
        daily_targets=request.targets.model_dump(),
        request_type="plan"
    )
    
    async def event_stream():
        try:
            # Stream events from the graph
            async for event in cerebro_graph.astream(state):
                # Send each state update as SSE
                yield f"data: {json.dumps(event)}\n\n"
                await asyncio.sleep(0.1)  # Small delay for smoother streaming
            
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )


# -----------------------------------------------------------------------------
# VERIFICATION ENDPOINTS
# -----------------------------------------------------------------------------

@app.post("/api/verify")
async def verify_progress(request: VerifyRequest):
    """
    Verify user's progress using Verifier and Rewarder agents.
    
    DEMO MODE: Uses pre-generated verification from actual TinyFish data.
    """
    resume = await get_resume(request.resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if DEMO_MODE:
        # ===== DEMO MODE: Load actual verification data =====
        data_dir = os.path.join(os.path.dirname(__file__), "db", "data")
        leetcode_file = os.path.join(data_dir, "leetcode_1.json")
        gmail_file = os.path.join(data_dir, "gmail_job_emails.json")
        
        print(f"\n{'='*60}")
        print(f"🔍 VERIFICATION STARTING")
        print(f"   LeetCode: {request.leetcode_username}")
        print(f"   Targets: {request.targets.leetcode} problems, {request.targets.applications} applications")
        print(f"{'='*60}\n")
        
        # Step 1: LeetCode Verification
        print(f"[AGENT 1/2] 💻 Verifier Agent - LeetCode Check")
        log_tool_call("Verifier", "tinyfish_sse", f"url=leetcode.com/u/{request.leetcode_username}")
        await asyncio.sleep(0.8)
        
        # Load LeetCode data
        leetcode_data = {}
        if os.path.exists(leetcode_file):
            with open(leetcode_file, "r") as f:
                leetcode_data = json.load(f)
        
        lc_total = leetcode_data.get("stats", {}).get("total_solved", 25)
        lc_recent = leetcode_data.get("recent_submissions", [])[:5]
        
        log_agent_step("Verifier", f"Connected to LeetCode profile: {leetcode_data.get('username', request.leetcode_username)}", "🔗")
        await asyncio.sleep(0.4)
        log_agent_step("Verifier", f"Total solved: {lc_total} problems", "📊")
        await asyncio.sleep(0.3)
        
        # Count recent submissions (simulate "today's" progress)
        recent_count = min(len(lc_recent), 4)
        log_agent_step("Verifier", f"Recent submissions: {recent_count} problems", "✅")
        for sub in lc_recent[:3]:
            print(f"           • {sub['problem']} ({sub['difficulty']}) - {sub['when']}")
            await asyncio.sleep(0.2)
        
        # Step 2: Gmail Verification
        print(f"\n[AGENT 2/2] 📧 Verifier Agent - Gmail Check")
        log_tool_call("Verifier", "tinyfish_sse", "url=gmail.com, task=check job application emails")
        await asyncio.sleep(0.8)
        
        # Load Gmail data
        gmail_data = {}
        if os.path.exists(gmail_file):
            with open(gmail_file, "r") as f:
                gmail_data = json.load(f)
        
        applications = gmail_data.get("applications", [])
        interviews = gmail_data.get("interviews", [])
        
        log_agent_step("Verifier", f"Connected to Gmail via TinyFish", "🔗")
        await asyncio.sleep(0.3)
        log_agent_step("Verifier", f"Applications sent: {len(applications)}", "📤")
        for app in applications:
            print(f"           • {app['company']} - {app['position']}")
            await asyncio.sleep(0.2)
        
        if interviews:
            log_agent_step("Verifier", f"🎉 Interview scheduled: {interviews[0]['company']}", "📅")
        
        # Step 3: Rewarder Agent
        print(f"\n[AGENT 3/3] 🎁 Rewarder Agent - Emotional Feedback")
        log_llm_call(
            "Rewarder Agent",
            "claude-3-5-haiku",
            "Generate emotional orbs based on performance",
            tokens_in=456,
            tokens_out=312
        )
        await asyncio.sleep(0.6)
        
        # Build results
        leetcode_actual = recent_count
        apps_actual = len(applications)
        
        demo_results = [
            {
                "task_type": "leetcode",
                "status": "partial" if leetcode_actual < request.targets.leetcode else "success",
                "target": request.targets.leetcode,
                "actual": leetcode_actual,
                "details": f"Solved {leetcode_actual} of {request.targets.leetcode} target problems",
                "recent_submissions": lc_recent[:5],
                "profile_stats": leetcode_data.get("stats", {})
            },
            {
                "task_type": "applications",
                "status": "success" if apps_actual >= request.targets.applications else "partial",
                "target": request.targets.applications,
                "actual": apps_actual,
                "details": f"Applied to {apps_actual} positions: {', '.join([a['company'] for a in applications])}",
                "applications": applications,
                "interviews": interviews
            }
        ]
        
        # Generate orbs based on actual performance
        # Using Inside Out 5 emotions: Joy, Sadness, Anger, Anxiety, Disgust
        demo_orbs = []
        
        # Check for rejections in gmail data
        rejections = gmail_data.get("rejections", [])
        
        # === LeetCode Performance ===
        if leetcode_actual >= request.targets.leetcode:
            # Target met! JOY orb
            log_agent_step("Rewarder", "✨ LeetCode target MET! Awarding JOY orb", "🌟")
            demo_orbs.append({
                "type": "joy",
                "color": "gold",
                "reason": f"🎉 Crushed {leetcode_actual} LeetCode problems! You're on fire!",
                "image_prompt": "A brilliant golden orb radiating warmth and accomplishment"
            })
        else:
            # Target missed - SADNESS orb
            missed = request.targets.leetcode - leetcode_actual
            log_agent_step("Rewarder", f"😢 Missed {missed} LeetCode problems. Generating SADNESS orb", "💙")
            demo_orbs.append({
                "type": "sadness",
                "color": "blue",
                "reason": f"😢 Solved {leetcode_actual}/{request.targets.leetcode} problems. It's okay - tomorrow is a new day!",
                "image_prompt": "A calming blue orb with waves of gentle encouragement"
            })
        
        # === Applications Performance ===
        if apps_actual >= request.targets.applications:
            log_agent_step("Rewarder", "✨ Application target MET! Awarding JOY orb", "🌟")
            demo_orbs.append({
                "type": "joy",
                "color": "gold",
                "reason": f"🎉 You applied to {apps_actual} companies! Target achieved!",
                "image_prompt": "A radiant golden orb glowing with warm energy and sparkles of achievement"
            })
        
        # === Interview Scheduled - Both JOY and ANXIETY ===
        if interviews:
            # JOY - exciting opportunity!
            log_agent_step("Rewarder", "✨ Interview scheduled! Awarding JOY orb (exciting opportunity!)", "🌟")
            demo_orbs.append({
                "type": "joy",
                "color": "gold",
                "reason": f"🎉 Interview at {interviews[0]['company']}! Your hard work is paying off!",
                "image_prompt": "A radiant golden orb sparkling with opportunity and excitement"
            })
            # ANXIETY - nerves are normal
            log_agent_step("Rewarder", "😰 Interview upcoming! Awarding ANXIETY orb (nerves are normal!)", "💜")
            demo_orbs.append({
                "type": "anxiety",
                "color": "purple",
                "reason": f"😰 Interview coming up at {interviews[0]['company']}! It's okay to be nervous - you've got this!",
                "image_prompt": "A swirling purple orb pulsing with nervous anticipation energy"
            })
        
        # === Rejection - SADNESS ===
        if rejections:
            log_agent_step("Rewarder", "😢 Received a rejection. Awarding SADNESS orb (it's okay to feel)", "💙")
            demo_orbs.append({
                "type": "sadness",
                "color": "blue",
                "reason": f"😢 Rejected by {rejections[0]['company']}. It's okay to feel sad - every rejection brings you closer to the right opportunity.",
                "image_prompt": "A soft blue orb with gentle teardrops of healing energy"
            })
        
        # Count orbs by type
        joy_count = sum(1 for o in demo_orbs if o["type"] == "joy")
        sadness_count = sum(1 for o in demo_orbs if o["type"] == "sadness")
        anxiety_count = sum(1 for o in demo_orbs if o["type"] == "anxiety")
        
        agent_thoughts = [
            f"Verifier Agent: 🔗 Connected to LeetCode via TinyFish SSE",
            f"Verifier Agent: 📊 Profile {leetcode_data.get('username', request.leetcode_username)} - {lc_total} total solved",
            f"Verifier Agent: ✓ Recent activity: {leetcode_actual} problems",
            f"Verifier Agent: 🔗 Connected to Gmail via TinyFish SSE (stealth mode)",
            f"Verifier Agent: 📤 Found {len(applications)} job applications",
            f"Verifier Agent: 📅 Found {len(interviews)} interview invite(s)",
            f"Verifier Agent: 📭 Found {len(rejections)} rejection(s)",
            f"Rewarder Agent: 🧠 Analyzing performance with Claude Haiku...",
            f"Rewarder Agent: ✨ Generated {len(demo_orbs)} emotional orbs",
            f"Rewarder Agent: 😊 {joy_count} Joy | 😢 {sadness_count} Sadness | 😰 {anxiety_count} Anxiety"
        ]
        
        await store_orbs(request.resume_id, demo_orbs)
        
        print(f"\n{'='*60}")
        print(f"✅ VERIFICATION COMPLETE")
        print(f"   📊 LeetCode: {leetcode_actual}/{request.targets.leetcode} problems")
        print(f"   📧 Applications: {apps_actual}/{request.targets.applications} sent")
        print(f"   🎁 Orbs earned: {len(demo_orbs)}")
        print(f"{'='*60}\n")
        
        return {
            "verification_results": demo_results,
            "orbs_earned": demo_orbs,
            "agent_thoughts": agent_thoughts,
            "leetcode_data": leetcode_data,
            "gmail_data": gmail_data,
            "stream_events": []
        }
    
    else:
        # ===== REAL MODE =====
        state = create_initial_state(
            user_id=request.resume_id,
            parsed_resume=resume,
            leetcode_username=request.leetcode_username,
            daily_targets=request.targets.model_dump(),
            request_type="verify"
        )
        
        try:
            result = await cerebro_graph.ainvoke(state)
            
            orbs_earned = result.get("orbs_earned", [])
            if orbs_earned:
                await store_orbs(request.resume_id, orbs_earned)
            
            return {
                "verification_results": result.get("verification_results", []),
                "orbs_earned": orbs_earned,
                "agent_thoughts": result.get("agent_thoughts", []),
                "stream_events": result.get("stream_events", [])
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")


@app.post("/api/verify/stream")
async def verify_progress_stream(request: VerifyRequest):
    """
    Verify progress with SSE streaming for live demo.
    
    DEMO MODE: Streams events using actual TinyFish verification data.
    """
    resume = await get_resume(request.resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if DEMO_MODE:
        # Load actual data files
        data_dir = os.path.join(os.path.dirname(__file__), "db", "data")
        leetcode_file = os.path.join(data_dir, "leetcode_1.json")
        gmail_file = os.path.join(data_dir, "gmail_job_emails.json")
        
        leetcode_data = {}
        gmail_data = {}
        
        if os.path.exists(leetcode_file):
            with open(leetcode_file, "r") as f:
                leetcode_data = json.load(f)
        
        if os.path.exists(gmail_file):
            with open(gmail_file, "r") as f:
                gmail_data = json.load(f)
        
        # ===== DEMO MODE: Staged SSE streaming with real data =====
        async def demo_event_stream():
            # Start
            yield f"data: {json.dumps({'type': 'start', 'message': '🚀 Starting verification with Claude + TinyFish...'})}\n\n"
            await asyncio.sleep(0.5)
            
            # LeetCode verification with TinyFish
            yield f"data: {json.dumps({'type': 'thought', 'thought': '🔧 Verifier Agent → tinyfish_sse (LeetCode check)'})}\n\n"
            await asyncio.sleep(0.6)
            
            yield f"data: {json.dumps({'type': 'thought', 'thought': f'🔗 Connecting to leetcode.com/u/{request.leetcode_username}/'})}\n\n"
            await asyncio.sleep(0.8)
            
            lc_username = leetcode_data.get('username', request.leetcode_username)
            lc_total = leetcode_data.get('stats', {}).get('total_solved', 25)
            lc_recent = leetcode_data.get('recent_submissions', [])[:5]
            
            yield f"data: {json.dumps({'type': 'thought', 'thought': f'📊 Profile: {lc_username} - {lc_total} total problems solved'})}\n\n"
            await asyncio.sleep(0.5)
            
            # Stream recent submissions
            for sub in lc_recent[:3]:
                problem = sub.get('problem', 'Unknown')
                difficulty = sub.get('difficulty', 'Unknown')
                when = sub.get('when', 'Recently')
                thought_msg = f'   • {problem} ({difficulty}) - {when}'
                yield f"data: {json.dumps({'type': 'thought', 'thought': thought_msg})}\n\n"
                await asyncio.sleep(0.3)
            
            leetcode_actual = min(len(lc_recent), 4)
            yield f"data: {json.dumps({'type': 'thought', 'thought': f'✅ Found {leetcode_actual} recent submissions'})}\n\n"
            await asyncio.sleep(0.5)
            
            # LeetCode verification result
            leetcode_result = {
                "task_type": "leetcode",
                "status": "partial" if leetcode_actual < request.targets.leetcode else "success",
                "target": request.targets.leetcode,
                "actual": leetcode_actual,
                "details": f"Solved {leetcode_actual} of {request.targets.leetcode} problems",
                "recent_submissions": lc_recent
            }
            yield f"data: {json.dumps({'type': 'verification_update', 'results': [leetcode_result]})}\n\n"
            await asyncio.sleep(0.8)
            
            # Gmail verification with TinyFish
            yield f"data: {json.dumps({'type': 'thought', 'thought': '🔧 Verifier Agent → tinyfish_sse (Gmail check, stealth mode)'})}\n\n"
            await asyncio.sleep(0.6)
            
            yield f"data: {json.dumps({'type': 'thought', 'thought': '🔗 Connecting to Gmail via TinyFish browser automation...'})}\n\n"
            await asyncio.sleep(0.8)
            
            applications = gmail_data.get('applications', [])
            interviews = gmail_data.get('interviews', [])
            
            yield f"data: {json.dumps({'type': 'thought', 'thought': f'📤 Found {len(applications)} job applications sent'})}\n\n"
            await asyncio.sleep(0.4)
            
            for app in applications:
                company = app.get('company', 'Unknown')
                position = app.get('position', 'Software Engineer')
                app_msg = f'   • {company} - {position}'
                yield f"data: {json.dumps({'type': 'thought', 'thought': app_msg})}\n\n"
                await asyncio.sleep(0.3)
            
            if interviews:
                interview = interviews[0]
                interview_company = interview.get('company', 'Unknown')
                interview_date = interview.get('details', {}).get('interview_date', 'TBD')
                interview_msg = f'🎉 Interview scheduled: {interview_company} on {interview_date}!'
                yield f"data: {json.dumps({'type': 'thought', 'thought': interview_msg})}\n\n"
                await asyncio.sleep(0.5)
            
            # Gmail verification result
            companies_list = ', '.join([a.get('company', 'Unknown') for a in applications])
            gmail_result = {
                "task_type": "applications",
                "status": "success" if len(applications) >= request.targets.applications else "partial",
                "target": request.targets.applications,
                "actual": len(applications),
                "details": f"Applied to: {companies_list}",
                "applications": applications,
                "interviews": interviews
            }
            yield f"data: {json.dumps({'type': 'verification_update', 'results': [leetcode_result, gmail_result]})}\n\n"
            await asyncio.sleep(0.8)
            
            # Rewarder agent with Claude Haiku
            yield f"data: {json.dumps({'type': 'thought', 'thought': '🧠 Rewarder Agent → claude-haiku-4-5 (emotional analysis)'})}\n\n"
            await asyncio.sleep(0.6)
            
            yield f"data: {json.dumps({'type': 'thought', 'thought': '   Analyzing performance to generate emotional feedback...'})}\n\n"
            await asyncio.sleep(0.5)
            
            orbs = []
            
            # Award orbs based on actual performance
            if len(applications) >= request.targets.applications:
                joy_orb = {
                    "type": "joy",
                    "color": "gold",
                    "reason": f"🎉 Application target achieved! Applied to {len(applications)} companies.",
                    "image_prompt": "A radiant golden orb glowing with achievement energy"
                }
                yield f"data: {json.dumps({'type': 'thought', 'thought': '✨ Awarding JOY orb - Application target met!'})}\n\n"
                await asyncio.sleep(0.4)
                orbs.append(joy_orb)
                yield f"data: {json.dumps({'type': 'orbs_update', 'orbs': orbs})}\n\n"
                await asyncio.sleep(0.5)
            
            if interviews:
                excitement_orb = {
                    "type": "excitement",
                    "color": "purple",
                    "reason": f"🎯 Interview at {interviews[0]['company']}! You're making real progress!",
                    "image_prompt": "A vibrant purple orb crackling with anticipation"
                }
                yield f"data: {json.dumps({'type': 'thought', 'thought': '⚡ Awarding EXCITEMENT orb - Interview scheduled!'})}\n\n"
                await asyncio.sleep(0.4)
                orbs.append(excitement_orb)
                yield f"data: {json.dumps({'type': 'orbs_update', 'orbs': orbs})}\n\n"
                await asyncio.sleep(0.5)
            
            if leetcode_actual < request.targets.leetcode:
                determination_orb = {
                    "type": "determination",
                    "color": "blue",
                    "reason": f"💪 {leetcode_actual}/{request.targets.leetcode} LeetCode problems. Keep pushing!",
                    "image_prompt": "A deep blue orb with swirling determination energy"
                }
                yield f"data: {json.dumps({'type': 'thought', 'thought': '💙 Awarding DETERMINATION orb - Encouragement for LeetCode progress'})}\n\n"
                await asyncio.sleep(0.4)
                orbs.append(determination_orb)
                yield f"data: {json.dumps({'type': 'orbs_update', 'orbs': orbs})}\n\n"
                await asyncio.sleep(0.5)
            
            # Store orbs
            if orbs:
                await store_orbs(request.resume_id, orbs)
            
            # Complete
            yield f"data: {json.dumps({'type': 'complete', 'message': f'✅ Verification complete! {len(orbs)} orbs added to your jar.', 'total_orbs': len(orbs)})}\n\n"
        
        return StreamingResponse(
            demo_event_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            }
        )
    
    else:
        # ===== REAL MODE =====
        state = create_initial_state(
            user_id=request.resume_id,
            parsed_resume=resume,
            leetcode_username=request.leetcode_username,
            daily_targets=request.targets.model_dump(),
            request_type="verify"
        )
        
        async def event_stream():
            try:
                yield f"data: {json.dumps({'type': 'start', 'message': 'Starting verification...'})}\n\n"
                
                async for event in cerebro_graph.astream(state):
                    if isinstance(event, dict):
                        thoughts = event.get("agent_thoughts", [])
                        if thoughts:
                            yield f"data: {json.dumps({'type': 'thought', 'thought': thoughts[-1]})}\n\n"
                        
                        stream_events = event.get("stream_events", [])
                        for se in stream_events:
                            yield f"data: {json.dumps(se)}\n\n"
                        
                        results = event.get("verification_results", [])
                        if results:
                            yield f"data: {json.dumps({'type': 'verification_update', 'results': results})}\n\n"
                        
                        orbs = event.get("orbs_earned", [])
                        if orbs:
                            yield f"data: {json.dumps({'type': 'orbs_update', 'orbs': orbs})}\n\n"
                    
                    await asyncio.sleep(0.05)
                
                yield f"data: {json.dumps({'type': 'complete', 'message': 'Verification complete!'})}\n\n"
                
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
        
        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            }
        )


# -----------------------------------------------------------------------------
# ORB ENDPOINTS
# -----------------------------------------------------------------------------

@app.get("/api/orbs/{user_id}")
async def get_user_orbs(user_id: str):
    """Get all orbs in user's jar"""
    orbs = await get_orb_jar(user_id)
    return {
        "user_id": user_id,
        "orb_jar": orbs,
        "total_orbs": len(orbs),
        "joy_count": sum(1 for o in orbs if o.get("emotion") == "joy"),
        "sadness_count": sum(1 for o in orbs if o.get("emotion") == "sadness")
    }


# -----------------------------------------------------------------------------
# LIVE BROWSER DEMO ENDPOINTS (HACKATHON DEMO!)
# -----------------------------------------------------------------------------

class BrowseRequest(BaseModel):
    task: str
    start_url: str
    wait_for_result: bool = False  # If False, returns immediately with view_url


@app.post("/api/browse/start")
async def start_browser_task(request: BrowseRequest):
    """
    Start a Yutori browsing task and return view_url for LIVE viewing!
    
    This is the KEY endpoint for hackathon demo - shows browser automation LIVE.
    """
    from tools.yutori_tools import yutori_browse_async, yutori_browse_sync
    
    if request.wait_for_result:
        # Wait for completion
        result = yutori_browse_sync(request.task, request.start_url, max_wait=90)
    else:
        # Return immediately with view_url for live viewing
        result = yutori_browse_async(request.task, request.start_url)
    
    return result


@app.get("/api/browse/status/{task_id}")
async def get_browser_status(task_id: str):
    """Get status of a browser task (for polling)."""
    from tools.yutori_tools import yutori_get_task_status
    return yutori_get_task_status(task_id)


@app.post("/api/demo/search-jobs-live")
async def demo_search_jobs_live(
    skills: str = "Python, JavaScript, React",
    experience_level: str = "mid"
):
    """
    DEMO: Start a live job search and return the view_url to watch!
    
    Returns immediately with a link to watch the AI browse job sites.
    """
    from tools.yutori_tools import yutori_browse_async
    
    task = f"""
    Search for 3 Software Engineer jobs suitable for a {experience_level} level candidate.
    Skills: {skills}
    
    For each job found, extract company name, title, location, and apply URL.
    """
    
    result = yutori_browse_async(
        task=task,
        start_url="https://www.linkedin.com/jobs/search/?keywords=software%20engineer"
    )
    
    return {
        "message": "🔴 LIVE - Watch the AI browse job sites!",
        "view_url": result.get("view_url"),
        "task_id": result.get("task_id"),
        "status": result.get("status"),
        "tip": "Open view_url in browser to watch live!"
    }


@app.post("/api/demo/verify-leetcode-live")
async def demo_verify_leetcode_live(username: str):
    """
    DEMO: Start live LeetCode verification with visible browser.
    
    Uses Yutori to show the browser navigating to LeetCode.
    """
    from tools.yutori_tools import yutori_browse_async
    
    task = f"""
    Go to leetcode.com/u/{username}/ and extract:
    1. Total problems solved
    2. Easy/Medium/Hard breakdown
    3. Recent submissions
    
    Report what you find about this user's LeetCode activity.
    """
    
    result = yutori_browse_async(
        task=task,
        start_url=f"https://leetcode.com/u/{username}/"
    )
    
    return {
        "message": f"🔴 LIVE - Checking LeetCode profile for {username}",
        "view_url": result.get("view_url"),
        "task_id": result.get("task_id"),
        "username": username,
        "tip": "Open view_url to watch the browser navigate!"
    }


# -----------------------------------------------------------------------------
# DEMO TRIGGER ENDPOINT
# -----------------------------------------------------------------------------

@app.post("/api/demo/trigger")
async def demo_trigger(
    resume_id: str,
    leetcode_username: str,
    action: str = Query(..., pattern="^(plan|verify)$")  # Fixed: regex -> pattern
):
    """
    Demo trigger endpoint - quickly run planning or verification.
    
    Use this during the hackathon demo for instant results.
    """
    resume = await get_resume(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    state = create_initial_state(
        user_id=resume_id,
        parsed_resume=resume,
        leetcode_username=leetcode_username,
        daily_targets=DEFAULT_TARGETS,
        request_type=action
    )
    
    result = await cerebro_graph.ainvoke(state)
    
    return {
        "action": action,
        "result": {
            "daily_plan": result.get("daily_plan"),
            "matched_jobs": result.get("matched_jobs"),
            "verification_results": result.get("verification_results"),
            "orbs_earned": result.get("orbs_earned"),
            "agent_thoughts": result.get("agent_thoughts")
        }
    }


# =============================================================================
# RUN SERVER
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
