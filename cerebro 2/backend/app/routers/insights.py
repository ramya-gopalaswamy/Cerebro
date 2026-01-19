"""Insights and analytics routes."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/weekly")
async def get_weekly_insights(user_id: str = "demo_user"):
    """Get weekly insights and analytics.
    
    TODO: Replace demo_user with actual Auth0 user_id from token.
    TODO: Implement analytics logic.
    """
    return {
        "message": "Insights endpoint - Analytics implementation pending",
        "orb_counts": {"gold": 0, "blue": 0, "red": 0},
        "completion_rate": 0.0,
        "insights": []
    }
