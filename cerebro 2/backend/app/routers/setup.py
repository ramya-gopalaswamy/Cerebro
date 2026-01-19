"""Setup route for initializing user state."""
from fastapi import APIRouter, HTTPException, status, Query
from datetime import datetime
from app.models.user import UserStateCreate, DailyTarget, UserState, OrbInventory
from app.storage.file_storage import storage
from app.services.task_service import task_service

router = APIRouter()


@router.post("/", name="setup_user")
async def setup_user(
    setup_data: UserStateCreate,
    user_id: str = Query("demo_user", description="User identifier")
):
    """Initialize user state with daily targets and generate initial tasks.
    
    Args:
        setup_data: Daily target configuration
        user_id: User identifier (TODO: from Auth0 token)
        
    Returns:
        Created user state.
    """
    # Check if user already exists
    if storage.user_exists(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already set up. Use /api/tasks/generate to generate new tasks."
        )
    
    # Generate initial tasks
    tasks = task_service.generate_tasks(setup_data.daily_target)
    tasks_dict = task_service.convert_tasks_to_dict(tasks)
    
    # Create user state
    user_state_dict = {
        "user_id": user_id,
        "daily_target": setup_data.daily_target.model_dump(),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "yesterday_tasks": [],
        "today_tasks": tasks_dict,
        "orb_inventory": {
            "gold": 0,
            "blue": 0,
            "red": 0
        },
        "task_history": []
    }
    
    # Save user state
    storage.save_user_state(user_id, user_state_dict)
    
    return {
        "message": "User setup completed successfully",
        "user_id": user_id,
        "daily_target": setup_data.daily_target.model_dump(),
        "tasks_generated": len(tasks_dict),
        "tasks": tasks_dict
    }
