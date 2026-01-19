"""War Room decision helper routes."""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class DecisionRequest(BaseModel):
    """Request model for decision helper."""
    question: str
    context: Optional[str] = None


@router.post("/decide")
async def make_decision(request: DecisionRequest, user_id: str = "demo_user"):
    """Get decision guidance from War Room.
    
    TODO: Replace demo_user with actual Auth0 user_id from token.
    TODO: Integrate LLM service for multi-perspective analysis.
    """
    return {
        "message": "War Room endpoint - LLM integration pending",
        "question": request.question,
        "recommendation": "Decision helper service coming soon"
    }
