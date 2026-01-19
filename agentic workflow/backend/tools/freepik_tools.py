"""
Freepik API Tools
Tools for generating orb images using Freepik Mystic API
"""
import requests
from typing import Literal
from langchain_core.tools import tool
import sys
sys.path.append('..')

from config import FREEPIK_API_KEY, FREEPIK_BASE_URL, ORB_PROMPTS


OrbEmotion = Literal["joy", "sadness", "anger", "anxiety", "disgust"]


@tool
def freepik_generate_orb(
    emotion: OrbEmotion,
    achievement: str,
    task_type: str
) -> dict:
    """
    Generate a unique orb image using Freepik Mystic API based on emotion and achievement.
    
    Args:
        emotion: The emotion for the orb - "joy", "sadness", "anger", "anxiety", or "logic"
        achievement: Description of what was achieved or missed
        task_type: Type of task (e.g., "leetcode", "application", "learning")
        
    Returns:
        Dictionary with generated orb image URL and metadata
    """
    # Get base prompt for emotion and customize with achievement
    base_prompt = ORB_PROMPTS.get(emotion, ORB_PROMPTS["logic"])
    
    # Add task-specific elements
    task_elements = {
        "leetcode": "coding symbols, algorithm patterns, binary code essence",
        "application": "email envelope, connection lines, networking energy",
        "learning": "book pages, knowledge streams, growth symbols",
        "interview": "conversation bubbles, handshake energy, opportunity glow"
    }
    
    task_detail = task_elements.get(task_type, "achievement symbols")
    
    full_prompt = f"{base_prompt}, {task_detail}, representing: {achievement}"
    
    try:
        response = requests.post(
            f"{FREEPIK_BASE_URL}/v1/ai/mystic",
            headers={
                "x-freepik-api-key": FREEPIK_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "prompt": full_prompt,
                "resolution": "2k",
                "aspect_ratio": "square_1_1",
                "model": "realism",
                "creative_detailing": 50,
                "filter_nsfw": True
            },
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        
        return {
            "success": True,
            "emotion": emotion,
            "task_type": task_type,
            "achievement": achievement,
            "image_url": result.get("data", [{}])[0].get("url") if result.get("data") else None,
            "prompt_used": full_prompt
        }
    except requests.RequestException as e:
        return {
            "success": False,
            "emotion": emotion,
            "task_type": task_type,
            "achievement": achievement,
            "error": str(e)
        }


def generate_orb_for_result(
    target_met: bool,
    count_achieved: int,
    count_target: int,
    task_type: str
) -> dict:
    """
    Helper function to determine emotion and generate appropriate orb.
    
    Args:
        target_met: Whether the target was met
        count_achieved: How many were completed
        count_target: What the target was
        task_type: Type of task
        
    Returns:
        Generated orb with appropriate emotion
    """
    # Determine emotion based on result
    if target_met:
        if count_achieved > count_target:
            # Exceeded target
            emotion = "joy"
            achievement = f"Crushed it! {count_achieved}/{count_target} {task_type} completed - exceeded target!"
        else:
            # Met target exactly
            emotion = "joy"
            achievement = f"Target met! {count_achieved}/{count_target} {task_type} completed"
    else:
        if count_achieved == 0:
            # No progress
            emotion = "sadness"
            achievement = f"Missed completely. 0/{count_target} {task_type} today."
        elif count_achieved >= count_target * 0.5:
            # Partial progress
            emotion = "sadness"
            achievement = f"Partial progress. {count_achieved}/{count_target} {task_type} - so close!"
        else:
            # Minimal progress
            emotion = "anger"
            achievement = f"Barely tried. {count_achieved}/{count_target} {task_type} - need to push harder!"
    
    # Use the tool to generate
    return freepik_generate_orb.invoke({
        "emotion": emotion,
        "achievement": achievement,
        "task_type": task_type
    })


# Emotion color mapping for frontend - Inside Out 5 emotions
ORB_COLORS = {
    "joy": {"primary": "#FFD700", "glow": "#FFA500"},      # Gold - Joy 😊
    "sadness": {"primary": "#5B8DD9", "glow": "#2E4A7D"},  # Blue - Sadness 😢
    "anger": {"primary": "#E53935", "glow": "#B71C1C"},    # Red - Anger 😤
    "anxiety": {"primary": "#9C27B0", "glow": "#7B1FA2"},  # Purple - Anxiety 😰
    "disgust": {"primary": "#4CAF50", "glow": "#388E3C"}   # Green - Disgust 🤢
}


def get_orb_color(emotion: OrbEmotion) -> dict:
    """Get color scheme for an emotion"""
    return ORB_COLORS.get(emotion, ORB_COLORS["joy"])
