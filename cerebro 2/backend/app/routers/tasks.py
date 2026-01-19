"""Task management routes."""
from fastapi import APIRouter, HTTPException, status, Request
from typing import List, Dict, Any
from datetime import datetime
from app.models.user import Task, UserStateCreate, DailyTarget, UserState, OrbInventory
from app.storage.file_storage import storage
from app.services.task_service import task_service

router = APIRouter()


@router.get("/today")
async def get_today_tasks(request: Request):
    """Get today's tasks for the user.
    
    TODO: Replace demo_user with actual Auth0 user_id from token.
    """
    user_id = request.headers.get("X-User-Id", "demo_user")
    user_state_dict = storage.get_user_state(user_id)
    if not user_state_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Please complete setup first."
        )
    
    return {
        "tasks": user_state_dict.get("today_tasks", []),
        "daily_target": user_state_dict.get("daily_target", {}),
        "orb_inventory": user_state_dict.get("orb_inventory", {"gold": 0, "blue": 0, "red": 0})
    }


@router.post("/generate")
async def generate_tasks(
    request: Request, keywords: str = "frontend developer"
):
    """Generate new tasks for today.
    
    Args:
        keywords: Job search keywords (default: "frontend developer")
        user_id: User identifier (TODO: from Auth0 token)
        
    Returns:
        Generated tasks list.
    """
    user_id = request.headers.get("X-User-Id", "demo_user")
    user_state_dict = storage.get_user_state(user_id)
    if not user_state_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Please complete setup first."
        )
    
    # Get daily target from user state
    daily_target_dict = user_state_dict.get("daily_target", {})
    daily_target = DailyTarget(**daily_target_dict)
    
    # Generate tasks
    tasks = task_service.generate_tasks(daily_target, keywords)
    
    # Convert to dictionaries for storage
    tasks_dict = task_service.convert_tasks_to_dict(tasks)
    
    # Update user state
    user_state_dict["today_tasks"] = tasks_dict
    user_state_dict["updated_at"] = datetime.utcnow().isoformat()
    
    storage.save_user_state(user_id, user_state_dict)
    
    return {
        "message": "Tasks generated successfully",
        "tasks": tasks_dict,
        "count": len(tasks_dict)
    }


@router.post("/reset")
async def reset_tasks(request: Request):
    """Reset tasks for a new day (move today to yesterday, generate new today).
    
    TODO: Replace demo_user with actual Auth0 user_id from token.
    """
    user_id = request.headers.get("X-User-Id", "demo_user")
    user_state_dict = storage.get_user_state(user_id)
    if not user_state_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Please complete setup first."
        )
    
    # Move today's tasks to yesterday
    user_state_dict["yesterday_tasks"] = user_state_dict.get("today_tasks", [])
    user_state_dict["today_tasks"] = []
    
    # Generate new tasks for today
    daily_target_dict = user_state_dict.get("daily_target", {})
    daily_target = DailyTarget(**daily_target_dict)
    
    tasks = task_service.generate_tasks(daily_target)
    tasks_dict = task_service.convert_tasks_to_dict(tasks)
    user_state_dict["today_tasks"] = tasks_dict
    
    # Update timestamp
    user_state_dict["updated_at"] = datetime.utcnow().isoformat()
    
    storage.save_user_state(user_id, user_state_dict)
    
    return {
        "message": "Tasks reset successfully",
        "today_tasks": tasks_dict,
        "yesterday_tasks": user_state_dict["yesterday_tasks"]
    }
