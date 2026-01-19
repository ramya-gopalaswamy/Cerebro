"""
LangGraph State Schema
Defines the state that flows through the agent graph
"""
from typing import TypedDict, List, Optional, Literal, Annotated
from operator import add


class JobMatch(TypedDict):
    """A matched job from Yutori"""
    company: str
    title: str
    location: Optional[str]
    salary_range: Optional[str]
    apply_url: Optional[str]
    match_reason: str
    skill_gaps: List[str]


class VerificationResult(TypedDict):
    """Result from TinyFish verification"""
    source: Literal["leetcode", "gmail"]
    success: bool
    count: int
    target: int
    details: Optional[dict]
    raw_result: Optional[str]


class Orb(TypedDict):
    """Generated orb reward"""
    emotion: Literal["joy", "sadness", "anger", "anxiety", "logic"]
    task_type: str
    reason: str
    image_url: Optional[str]
    colors: dict


class DailyPlan(TypedDict):
    """Daily preparation plan"""
    date: str
    leetcode: dict  # target, difficulty_mix, topics, reasoning
    applications: dict  # target, job_types, reasoning
    learning_tasks: List[dict]
    summary: str


class AgentState(TypedDict):
    """
    Main state that flows through the LangGraph.
    All agents read from and write to this state.
    """
    # ===== User Context =====
    user_id: str
    parsed_resume: dict  # Full ParsedResume from resume module
    leetcode_username: str
    daily_targets: dict  # {"leetcode": 5, "applications": 2}
    
    # ===== Request Info =====
    request_type: Literal["plan", "verify", "research"]
    
    # ===== Planner Output =====
    daily_plan: Optional[DailyPlan]
    
    # ===== Job Matcher Output =====
    matched_jobs: Annotated[List[JobMatch], add]  # Accumulated
    job_search_query: Optional[str]
    
    # ===== Verifier Output =====
    verification_results: Annotated[List[VerificationResult], add]  # Accumulated
    leetcode_verified: Optional[bool]
    gmail_verified: Optional[bool]
    
    # ===== Rewarder Output =====
    orbs_earned: Annotated[List[Orb], add]  # Accumulated
    
    # ===== Agent Reasoning Trail =====
    agent_thoughts: Annotated[List[str], add]  # All agent thoughts
    current_agent: Optional[str]
    
    # ===== Streaming Events =====
    stream_events: Annotated[List[dict], add]  # For SSE streaming
    
    # ===== Control Flow =====
    next_action: Optional[str]
    should_continue: bool
    error: Optional[str]


def create_initial_state(
    user_id: str,
    parsed_resume: dict,
    leetcode_username: str,
    daily_targets: dict,
    request_type: Literal["plan", "verify", "research"] = "plan"
) -> AgentState:
    """
    Create a fresh initial state for the graph.
    
    Args:
        user_id: Unique user identifier
        parsed_resume: Parsed resume data
        leetcode_username: LeetCode username for verification
        daily_targets: Daily targets dict
        request_type: What the user is requesting
        
    Returns:
        Initial AgentState
    """
    return AgentState(
        user_id=user_id,
        parsed_resume=parsed_resume,
        leetcode_username=leetcode_username,
        daily_targets=daily_targets,
        request_type=request_type,
        daily_plan=None,
        matched_jobs=[],
        job_search_query=None,
        verification_results=[],
        leetcode_verified=None,
        gmail_verified=None,
        orbs_earned=[],
        agent_thoughts=[],
        current_agent=None,
        stream_events=[],
        next_action=None,
        should_continue=True,
        error=None
    )
