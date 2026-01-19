"""Verification routes for progress checking."""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from datetime import datetime, timedelta
from app.storage.file_storage import storage
from app.services.gmail_service import gmail_service
from app.services.leetcode_service import leetcode_service
from app.services.orb_service import orb_service
from app.agents.joy_agent import joy_agent
from app.agents.sadness_agent import sadness_agent
from app.agents.logic_agent import logic_agent
from app.models.user import DailyTarget

router = APIRouter()


@router.get("/check-progress")
async def check_progress(
    user_id: str = "demo_user",
    timeframe_hours: int = 24
):
    """Morning routine: Check progress and award orbs.
    
    Args:
        user_id: User identifier (TODO: from Auth0 token)
        timeframe_hours: Hours to look back (default: 24)
        
    Returns:
        Verification results with orbs awarded and messages.
    """
    # Get user state
    user_state = storage.get_user_state(user_id)
    if not user_state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Please complete setup first."
        )
    
    # Get daily targets
    daily_target_dict = user_state.get("daily_target", {})
    daily_target = DailyTarget(**daily_target_dict)
    
    # Check Gmail for sent applications
    apps_sent = gmail_service.count_sent_emails(
        timeframe_hours=timeframe_hours,
        keywords=gmail_service.application_keywords
    )
    
    # Check LeetCode for submissions
    leetcode_username = user_state.get("leetcode_username")  # Optional field
    leetcode_done = leetcode_service.check_user_submission(
        username=leetcode_username,
        timeframe_hours=timeframe_hours
    )
    
    # Generate orbs based on results
    orbs_dict, messages_dict = orb_service.generate_orbs(
        apps_sent=apps_sent,
        apps_target=daily_target.apps,
        leetcode_done=leetcode_done,
        leetcode_target=daily_target.leetcode
    )
    
    # Get agent messages
    agent_messages = {}
    if orbs_dict.get("gold", 0) > 0:
        agent_messages["joy"] = joy_agent.speak(context="success", max_words=20)
    
    if orbs_dict.get("blue", 0) > 0:
        agent_messages["sadness"] = sadness_agent.speak(context="missed", max_words=20)
    
    # Get logic analysis
    total_tasks = daily_target.apps + daily_target.leetcode
    completed_tasks = (1 if apps_sent >= daily_target.apps else 0) + (1 if leetcode_done else 0)
    completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0.0
    
    analysis = logic_agent.analyze_progress(
        apps_sent=apps_sent,
        apps_target=daily_target.apps,
        leetcode_done=leetcode_done,
        leetcode_target=daily_target.leetcode,
        completion_rate=completion_rate
    )
    agent_messages["logic"] = logic_agent.speak(analysis, max_words=30)
    
    # Update user state with new orbs
    current_inventory = user_state.get("orb_inventory", {"gold": 0, "blue": 0, "red": 0})
    updated_inventory = orb_service.add_orbs_to_inventory(current_inventory, orbs_dict)
    user_state["orb_inventory"] = updated_inventory
    user_state["updated_at"] = datetime.utcnow().isoformat()
    
    # Save updated state
    storage.save_user_state(user_id, user_state)
    
    return {
        "verification": {
            "apps_sent": apps_sent,
            "apps_target": daily_target.apps,
            "leetcode_done": leetcode_done,
            "leetcode_target": daily_target.leetcode,
            "completion_rate": completion_rate,
        },
        "orbs_awarded": orbs_dict,
        "orb_inventory": updated_inventory,
        "messages": {
            **agent_messages,
            "orb_messages": messages_dict,
        },
        "analysis": analysis,
    }
