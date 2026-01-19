"""
LLM Factory - Creates LLM instances using Anthropic API
"""
from typing import Literal
from langchain_anthropic import ChatAnthropic
from config import (
    ANTHROPIC_CONFIG,
    AGENT_MODELS
)


def get_llm(model_type: Literal["sonnet", "haiku"] = "sonnet"):
    """
    Get an LLM instance using Anthropic API.
    
    Args:
        model_type: "sonnet" for complex tasks, "haiku" for simple tasks
        
    Returns:
        LangChain ChatAnthropic instance
    """
    model = ANTHROPIC_CONFIG["sonnet_model"] if model_type == "sonnet" else ANTHROPIC_CONFIG["haiku_model"]
    return ChatAnthropic(
        api_key=ANTHROPIC_CONFIG["api_key"],
        model=model,
        temperature=0.7,
        max_tokens=2048
    )


def get_agent_llm(agent_name: str):
    """
    Get the appropriate LLM for a specific agent.
    
    Args:
        agent_name: One of "resume_parser", "planner", "job_matcher", "verifier", "rewarder"
        
    Returns:
        LangChain ChatModel instance configured for that agent
    """
    model_type = AGENT_MODELS.get(agent_name, "sonnet")
    return get_llm(model_type)


# Pre-configured LLMs for convenience
def get_sonnet():
    """Get Sonnet model for complex reasoning tasks"""
    return get_llm("sonnet")


def get_haiku():
    """Get Haiku model for fast, simple tasks"""
    return get_llm("haiku")
