"""
Simple Storage
File-based storage for resumes and user data (for hackathon demo)
"""
import json
import os
from typing import Optional
from datetime import datetime
import uuid


# Storage directory
STORAGE_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(STORAGE_DIR, exist_ok=True)


def _get_resume_path(resume_id: str) -> str:
    return os.path.join(STORAGE_DIR, f"resume_{resume_id}.json")


def _get_user_path(user_id: str) -> str:
    return os.path.join(STORAGE_DIR, f"user_{user_id}.json")


async def store_resume(parsed_resume: dict) -> str:
    """
    Store a parsed resume and return its ID.
    """
    resume_id = str(uuid.uuid4())[:8]
    
    data = {
        "id": resume_id,
        "created_at": datetime.now().isoformat(),
        "resume": parsed_resume
    }
    
    path = _get_resume_path(resume_id)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    
    return resume_id


async def get_resume(resume_id: str) -> Optional[dict]:
    """
    Retrieve a stored resume by ID.
    """
    path = _get_resume_path(resume_id)
    
    if not os.path.exists(path):
        return None
    
    with open(path, "r") as f:
        data = json.load(f)
    
    return data.get("resume")


async def store_user_state(user_id: str, state: dict) -> None:
    """
    Store user state (for persistence across sessions).
    """
    path = _get_user_path(user_id)
    
    existing = {}
    if os.path.exists(path):
        with open(path, "r") as f:
            existing = json.load(f)
    
    existing.update(state)
    existing["updated_at"] = datetime.now().isoformat()
    
    with open(path, "w") as f:
        json.dump(existing, f, indent=2)


async def get_user_state(user_id: str) -> Optional[dict]:
    """
    Retrieve user state.
    """
    path = _get_user_path(user_id)
    
    if not os.path.exists(path):
        return None
    
    with open(path, "r") as f:
        return json.load(f)


async def store_orbs(user_id: str, orbs: list) -> None:
    """
    Append orbs to user's orb jar.
    """
    state = await get_user_state(user_id) or {}
    existing_orbs = state.get("orb_jar", [])
    existing_orbs.extend(orbs)
    state["orb_jar"] = existing_orbs
    await store_user_state(user_id, state)


async def get_orb_jar(user_id: str) -> list:
    """
    Get all orbs for a user.
    """
    state = await get_user_state(user_id)
    if not state:
        return []
    return state.get("orb_jar", [])


# Initialize storage directory
def init_storage():
    """Ensure storage directory exists"""
    os.makedirs(STORAGE_DIR, exist_ok=True)
    os.makedirs(os.path.join(STORAGE_DIR, "data"), exist_ok=True)


init_storage()
