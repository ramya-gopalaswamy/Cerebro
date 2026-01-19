"""
Rewarder Agent
Evaluates results and awards orbs using Freepik
Uses Inside Out 5 core emotions: Joy, Sadness, Anger, Anxiety, Disgust
"""
import sys
sys.path.append('..')

from llm_factory import get_agent_llm
from graph.state import AgentState, Orb
from tools.freepik_tools import freepik_generate_orb, generate_orb_for_result, get_orb_color


REWARDER_SYSTEM_PROMPT = """You are the Rewarder Agent for Cerebro, an AI job preparation coach.

Your job is to evaluate the user's verification results and award appropriate orbs.

Orb Types (Inside Out emotions):
- JOY (gold): Target met or exceeded - celebrate the achievement! 😊
- SADNESS (blue): Target missed, rejection received - acknowledge the feeling, it's okay to be sad 😢
- ANGER (red): Pattern of avoidance, not pushing hard enough - motivate change 😤
- ANXIETY (purple): High-pressure situation (interview scheduled) - acknowledge the nerves 😰
- DISGUST (green): Bad job fit, something doesn't feel right - trust your instincts 🤢

For each verification result (LeetCode, Gmail), decide:
1. Which emotion best fits the outcome
2. A short reason explaining the orb
3. Whether this is a positive or constructive feedback moment

Be emotionally intelligent - sometimes missing a target by 1 deserves encouragement, not sadness.
Interviews are exciting but also nerve-wracking - anxiety is a natural response!
Rejections hurt - let sadness validate the user's feelings before encouraging them.
"""


async def rewarder_agent(state: AgentState) -> AgentState:
    """
    Rewarder agent node - awards orbs based on verification results.
    
    Reads: verification_results, daily_targets
    Writes: orbs_earned, agent_thoughts
    """
    llm = get_agent_llm("rewarder")
    
    results = state.get("verification_results", [])
    targets = state.get("daily_targets", {"leetcode": 5, "applications": 2})
    orbs_earned = []
    
    state["current_agent"] = "rewarder"
    state["agent_thoughts"].append("Rewarder Agent: Evaluating results and generating orb rewards...")
    
    for result in results:
        source = result.get("source", "unknown")
        count = result.get("count", 0)
        target = result.get("target", 5)
        success = result.get("success", False)
        
        # Check for special situations
        has_interview = result.get("has_interview", False)
        has_rejection = result.get("has_rejection", False)
        interview_company = result.get("interview_company", "")
        rejection_company = result.get("rejection_company", "")
        
        # Handle interview scheduled - Anxiety orb
        if has_interview:
            emotion = "anxiety"
            reason = f"😰 Interview scheduled at {interview_company}! It's okay to feel nervous - you've got this!"
            
            state["agent_thoughts"].append(f"Rewarder Agent: Generating ANXIETY orb for interview at {interview_company}...")
            state["stream_events"].append({
                "type": "orb_generating",
                "emotion": emotion,
                "source": "interview"
            })
            
            try:
                orb_result = freepik_generate_orb.invoke({
                    "emotion": emotion,
                    "achievement": reason,
                    "task_type": "interview"
                })
                image_url = orb_result.get("image_url") if orb_result.get("success") else None
            except Exception as e:
                state["agent_thoughts"].append(f"Rewarder Agent: Orb generation error - {str(e)}")
                image_url = None
            
            interview_orb = {
                "emotion": emotion,
                "task_type": "interview",
                "reason": reason,
                "image_url": image_url,
                "colors": get_orb_color(emotion),
            }
            orbs_earned.append(interview_orb)
            state["agent_thoughts"].append(f"Rewarder Agent: Awarded ANXIETY orb for interview - nerves are totally normal!")
        
        # Handle rejection - Sadness orb
        if has_rejection:
            emotion = "sadness"
            reason = f"😢 Rejected by {rejection_company}. It's okay to feel sad - every rejection brings you closer to the right opportunity."
            
            state["agent_thoughts"].append(f"Rewarder Agent: Generating SADNESS orb for rejection from {rejection_company}...")
            state["stream_events"].append({
                "type": "orb_generating",
                "emotion": emotion,
                "source": "rejection"
            })
            
            try:
                orb_result = freepik_generate_orb.invoke({
                    "emotion": emotion,
                    "achievement": reason,
                    "task_type": "rejection"
                })
                image_url = orb_result.get("image_url") if orb_result.get("success") else None
            except Exception as e:
                state["agent_thoughts"].append(f"Rewarder Agent: Orb generation error - {str(e)}")
                image_url = None
            
            rejection_orb = {
                "emotion": emotion,
                "task_type": "rejection",
                "reason": reason,
                "image_url": image_url,
                "colors": get_orb_color(emotion),
            }
            orbs_earned.append(rejection_orb)
            state["agent_thoughts"].append(f"Rewarder Agent: Awarded SADNESS orb - it's okay to feel your feelings 💙")
        
        # Determine emotion and reason for task completion
        if not success:
            # Verification failed - gentle feedback
            emotion = "anxiety"
            reason = f"😰 Couldn't verify {source} - technical issue. Don't worry, we'll try again."
        elif count >= target:
            if count > target:
                emotion = "joy"
                reason = f"🎉 EXCEEDED target! {count}/{target} {source} - you're crushing it!"
            else:
                emotion = "joy"
                reason = f"✨ Target MET! {count}/{target} {source} - great discipline!"
        elif count >= target * 0.8:
            # Close to target
            emotion = "sadness"
            reason = f"😢 So close! {count}/{target} {source} - just a bit more next time."
        elif count >= target * 0.5:
            # Partial progress
            emotion = "sadness"
            reason = f"😢 Partial progress. {count}/{target} {source} - the journey continues."
        elif count > 0:
            # Minimal progress
            emotion = "anger"
            reason = f"😤 Only {count}/{target} {source}. We can do better. Let's push harder!"
        else:
            # No progress
            emotion = "sadness"
            reason = f"😢 No {source} progress today. Tomorrow is a new opportunity."
        
        # Generate orb using Freepik
        state["agent_thoughts"].append(f"Rewarder Agent: Generating {emotion.upper()} orb for {source}...")
        state["stream_events"].append({
            "type": "orb_generating",
            "emotion": emotion,
            "source": source
        })
        
        try:
            orb_result = freepik_generate_orb.invoke({
                "emotion": emotion,
                "achievement": reason,
                "task_type": source
            })
            
            image_url = orb_result.get("image_url") if orb_result.get("success") else None
        except Exception as e:
            state["agent_thoughts"].append(f"Rewarder Agent: Orb generation error - {str(e)}")
            image_url = None
        
        # Create orb object
        orb = {
            "emotion": emotion,
            "task_type": source,
            "reason": reason,
            "image_url": image_url,
            "colors": get_orb_color(emotion),
            "count": count,
            "target": target
        }
        
        orbs_earned.append(orb)
        state["agent_thoughts"].append(f"Rewarder Agent: Awarded {emotion.upper()} orb for {source} - {reason}")
        state["stream_events"].append({
            "type": "orb_awarded",
            "orb": orb
        })
    
    # Update state
    state["orbs_earned"] = orbs_earned
    state["stream_events"].append({
        "type": "agent_complete",
        "agent": "rewarder",
        "output": {"orbs": orbs_earned}
    })
    
    # Final summary
    joy_count = sum(1 for o in orbs_earned if o["emotion"] == "joy")
    sadness_count = sum(1 for o in orbs_earned if o["emotion"] == "sadness")
    anxiety_count = sum(1 for o in orbs_earned if o["emotion"] == "anxiety")
    total = len(orbs_earned)
    
    summary_parts = []
    if joy_count > 0:
        summary_parts.append(f"{joy_count} JOY 😊")
    if sadness_count > 0:
        summary_parts.append(f"{sadness_count} SADNESS 😢")
    if anxiety_count > 0:
        summary_parts.append(f"{anxiety_count} ANXIETY 😰")
    
    state["agent_thoughts"].append(f"Rewarder Agent: Awarded {total} orbs today: {', '.join(summary_parts)}. Remember, all emotions are valid!")
    
    return state
