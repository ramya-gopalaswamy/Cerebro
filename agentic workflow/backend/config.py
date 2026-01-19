"""
Configuration for Cerebro JobLand Backend
API keys and model configuration for Anthropic, Yutori, TinyFish, Freepik
"""
import os

# =============================================================================
# LLM PROVIDER CONFIGURATION
# =============================================================================

# Anthropic API Configuration
ANTHROPIC_CONFIG = {
    "api_key": os.getenv("ANTHROPIC_API_KEY", ""),
    "sonnet_model": "claude-sonnet-4-20250514",
    "haiku_model": "claude-3-5-haiku-20241022"
}

# =============================================================================
# EXTERNAL API KEYS
# =============================================================================

# Yutori API (Job Search & Research)
YUTORI_API_KEY = os.getenv("YUTORI_API_KEY", "your-yutori-key")
YUTORI_BASE_URL = "https://api.yutori.com"

# TinyFish API (Browser Automation)
TINYFISH_API_KEY = os.getenv("TINYFISH_API_KEY", "your-tinyfish-key")
TINYFISH_BASE_URL = "https://mino.ai"

# Freepik API (Orb Image Generation)
FREEPIK_API_KEY = os.getenv("FREEPIK_API_KEY", "your-freepik-key")
FREEPIK_BASE_URL = "https://api.freepik.com"

# =============================================================================
# AGENT MODEL ASSIGNMENTS
# =============================================================================

# Which model each agent should use
AGENT_MODELS = {
    "resume_parser": "sonnet",    # Complex extraction
    "planner": "sonnet",          # Personalized planning
    "job_matcher": "sonnet",      # Skill matching
    "verifier": "haiku",          # Simple tool invocation
    "rewarder": "haiku"           # Simple emotion decision
}

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================

# Default daily targets
DEFAULT_TARGETS = {
    "leetcode": 5,
    "applications": 2
}

# Job search focus
JOB_SEARCH_ROLE = "Software Engineer"

# Orb emotion prompts for Freepik
ORB_PROMPTS = {
    "joy": "Golden glowing magical orb, warm radiant light, celebrating achievement, fantasy art style, mystical energy",
    "sadness": "Blue ethereal orb, soft melancholic glow, gentle sadness, dreamy art style, floating tears essence",
    "anger": "Red fierce orb, flame essence, burning determination, dramatic art style, powerful energy",
    "anxiety": "Purple swirling orb, electric energy, urgency and tension, mystical art style, nervous sparks",
    "logic": "Cyan crystalline orb, geometric patterns, clarity and insight, futuristic art style, data streams"
}
