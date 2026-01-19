"""
Tools Module
LangChain tools for external API integrations

APIs Used:
- Yutori: Browsing (job search, research), Scouting (monitoring)
- TinyFish: Browser automation (LeetCode, Gmail)
- Freepik: Image generation (Orbs)
"""
from tools.yutori_tools import (
    yutori_search_jobs,
    yutori_research_company,
    yutori_create_job_scout,
    yutori_browse,
    yutori_get_task_status
)

from tools.tinyfish_tools import (
    tinyfish_get_leetcode_problems,
    tinyfish_verify_leetcode,
    tinyfish_check_gmail_sent,
    tinyfish_search_jobs,
    tinyfish_leetcode_stream,
    tinyfish_gmail_stream
)

from tools.freepik_tools import (
    freepik_generate_orb,
    generate_orb_for_result,
    get_orb_color,
    ORB_COLORS
)

# All tools for agent binding
ALL_TOOLS = [
    # Yutori tools
    yutori_search_jobs,
    yutori_research_company,
    yutori_create_job_scout,
    # TinyFish tools
    tinyfish_get_leetcode_problems,
    tinyfish_verify_leetcode,
    tinyfish_check_gmail_sent,
    tinyfish_search_jobs,
    # Freepik tools
    freepik_generate_orb
]

# Grouped by function
JOB_TOOLS = [yutori_search_jobs, yutori_research_company, tinyfish_search_jobs]
LEETCODE_TOOLS = [tinyfish_get_leetcode_problems, tinyfish_verify_leetcode]
VERIFICATION_TOOLS = [tinyfish_verify_leetcode, tinyfish_check_gmail_sent]
REWARD_TOOLS = [freepik_generate_orb]

__all__ = [
    # Yutori
    "yutori_search_jobs",
    "yutori_research_company",
    "yutori_create_job_scout",
    "yutori_browse",
    "yutori_get_task_status",
    # TinyFish
    "tinyfish_get_leetcode_problems",
    "tinyfish_verify_leetcode",
    "tinyfish_check_gmail_sent",
    "tinyfish_search_jobs",
    "tinyfish_leetcode_stream",
    "tinyfish_gmail_stream",
    # Freepik
    "freepik_generate_orb",
    "generate_orb_for_result",
    "get_orb_color",
    "ORB_COLORS",
    # Tool groups
    "ALL_TOOLS",
    "JOB_TOOLS",
    "LEETCODE_TOOLS",
    "VERIFICATION_TOOLS",
    "REWARD_TOOLS"
]
