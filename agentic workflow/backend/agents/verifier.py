"""
Verifier Agent
Verifies user's actual progress using TinyFish browser automation
"""
import sys
sys.path.append('..')

from llm_factory import get_agent_llm
from graph.state import AgentState, VerificationResult
from tools.tinyfish_tools import tinyfish_verify_leetcode, tinyfish_check_gmail_sent


VERIFIER_SYSTEM_PROMPT = """You are the Verifier Agent for Cerebro, an AI job preparation coach.

Your job is to verify if the user actually completed their daily tasks.

You have access to:
1. tinyfish_verify_leetcode - Check LeetCode profile for submissions
2. tinyfish_check_gmail - Check Gmail for job application emails

Be factual and report exactly what you find. Don't assume or guess.
If verification fails, report the error honestly.

After verification, summarize:
- How many LeetCode problems were solved vs target
- How many job applications were sent vs target
- Any interesting patterns (all easy? specific topics?)
"""


async def verifier_agent(state: AgentState) -> AgentState:
    """
    Verifier agent node - checks LeetCode and Gmail using TinyFish.
    
    Reads: leetcode_username, daily_targets
    Writes: verification_results, agent_thoughts
    """
    llm = get_agent_llm("verifier")
    
    username = state.get("leetcode_username", "")
    targets = state.get("daily_targets", {"leetcode": 5, "applications": 2})
    
    verification_results = []
    
    # ===== VERIFY LEETCODE =====
    state["agent_thoughts"].append(f"Verifier Agent: Checking LeetCode profile for user '{username}'...")
    state["current_agent"] = "verifier"
    state["stream_events"].append({
        "type": "verification_start",
        "source": "leetcode",
        "username": username
    })
    
    try:
        leetcode_result = tinyfish_verify_leetcode.invoke({"username": username})
        
        # Parse result
        if leetcode_result.get("success"):
            # Extract count from result
            result_data = leetcode_result.get("result", {})
            if isinstance(result_data, str):
                # Try to parse count from text
                import re
                match = re.search(r'(\d+)\s*problem', result_data.lower())
                lc_count = int(match.group(1)) if match else 0
            elif isinstance(result_data, dict):
                lc_count = result_data.get("problems_solved_today", 0)
            else:
                lc_count = 0
            
            verification_results.append({
                "source": "leetcode",
                "success": True,
                "count": lc_count,
                "target": targets.get("leetcode", 5),
                "details": result_data,
                "raw_result": leetcode_result.get("result")
            })
            state["agent_thoughts"].append(f"Verifier Agent: LeetCode check complete. Found {lc_count} problems solved today.")
            state["leetcode_verified"] = True
        else:
            verification_results.append({
                "source": "leetcode",
                "success": False,
                "count": 0,
                "target": targets.get("leetcode", 5),
                "details": {"error": leetcode_result.get("error", "Unknown error")},
                "raw_result": None
            })
            state["agent_thoughts"].append(f"Verifier Agent: LeetCode check failed - {leetcode_result.get('error', 'Unknown error')}")
            state["leetcode_verified"] = False
            
    except Exception as e:
        verification_results.append({
            "source": "leetcode",
            "success": False,
            "count": 0,
            "target": targets.get("leetcode", 5),
            "details": {"error": str(e)},
            "raw_result": None
        })
        state["agent_thoughts"].append(f"Verifier Agent: LeetCode exception - {str(e)}")
        state["leetcode_verified"] = False
    
    state["stream_events"].append({
        "type": "verification_complete",
        "source": "leetcode",
        "result": verification_results[-1]
    })
    
    # ===== VERIFY GMAIL =====
    state["agent_thoughts"].append("Verifier Agent: Checking Gmail for job applications...")
    state["stream_events"].append({
        "type": "verification_start",
        "source": "gmail"
    })
    
    try:
        gmail_result = tinyfish_check_gmail_sent.invoke({})
        
        if gmail_result.get("success"):
            result_data = gmail_result.get("result", {})
            if isinstance(result_data, str):
                import re
                match = re.search(r'(\d+)', result_data)
                gmail_count = int(match.group(1)) if match else 0
            elif isinstance(result_data, dict):
                gmail_count = result_data.get("applications_sent", 0)
            else:
                gmail_count = 0
            
            verification_results.append({
                "source": "gmail",
                "success": True,
                "count": gmail_count,
                "target": targets.get("applications", 2),
                "details": result_data,
                "raw_result": gmail_result.get("result")
            })
            state["agent_thoughts"].append(f"Verifier Agent: Gmail check complete. Found {gmail_count} applications sent today.")
            state["gmail_verified"] = True
        else:
            verification_results.append({
                "source": "gmail",
                "success": False,
                "count": 0,
                "target": targets.get("applications", 2),
                "details": {"error": gmail_result.get("error", "Unknown error")},
                "raw_result": None
            })
            state["agent_thoughts"].append(f"Verifier Agent: Gmail check failed - {gmail_result.get('error', 'Unknown error')}")
            state["gmail_verified"] = False
            
    except Exception as e:
        verification_results.append({
            "source": "gmail",
            "success": False,
            "count": 0,
            "target": targets.get("applications", 2),
            "details": {"error": str(e)},
            "raw_result": None
        })
        state["agent_thoughts"].append(f"Verifier Agent: Gmail exception - {str(e)}")
        state["gmail_verified"] = False
    
    state["stream_events"].append({
        "type": "verification_complete",
        "source": "gmail",
        "result": verification_results[-1]
    })
    
    # Update state
    state["verification_results"] = verification_results
    state["stream_events"].append({
        "type": "agent_complete",
        "agent": "verifier",
        "output": {"results": verification_results}
    })
    
    return state
