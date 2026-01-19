"""User state models for Cerebro."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class DailyTarget(BaseModel):
    """Daily target configuration."""
    apps: int = Field(ge=0, description="Number of job applications per day")
    leetcode: int = Field(ge=0, description="Number of LeetCode problems per day")


class Task(BaseModel):
    """Individual task item."""
    id: str
    type: str = Field(description="Task type: 'job' or 'leetcode'")
    title: str
    url: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed: bool = False
    completed_at: Optional[datetime] = None


class OrbInventory(BaseModel):
    """Orb inventory counts."""
    gold: int = Field(default=0, ge=0, description="Gold orbs (success)")
    blue: int = Field(default=0, ge=0, description="Blue orbs (missed)")
    red: int = Field(default=0, ge=0, description="Red orbs (critical)")


class TaskHistory(BaseModel):
    """Historical task record."""
    date: str
    tasks: List[Task]
    apps_completed: int
    leetcode_completed: int
    orbs_awarded: OrbInventory
    completion_rate: float = Field(ge=0.0, le=1.0)


class UserState(BaseModel):
    """Complete user state model."""
    user_id: str = Field(description="Auth0 user identifier")
    daily_target: DailyTarget
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    yesterday_tasks: List[Task] = Field(default_factory=list)
    today_tasks: List[Task] = Field(default_factory=list)
    orb_inventory: OrbInventory = Field(default_factory=OrbInventory)
    task_history: List[TaskHistory] = Field(default_factory=list)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserStateCreate(BaseModel):
    """Schema for creating user state."""
    daily_target: DailyTarget


class UserStateResponse(BaseModel):
    """Schema for user state API response."""
    user_id: str
    daily_target: DailyTarget
    created_at: str
    updated_at: str
    today_tasks: List[Task]
    orb_inventory: OrbInventory
    task_history_count: int
    
    @classmethod
    def from_user_state(cls, state: UserState) -> "UserStateResponse":
        """Create response model from UserState."""
        return cls(
            user_id=state.user_id,
            daily_target=state.daily_target,
            created_at=state.created_at.isoformat(),
            updated_at=state.updated_at.isoformat(),
            today_tasks=state.today_tasks,
            orb_inventory=state.orb_inventory,
            task_history_count=len(state.task_history),
        )
