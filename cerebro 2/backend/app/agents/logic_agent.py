"""Logic agent for rational analysis."""
from typing import Dict, Optional, List


class LogicAgent:
    """Handles rational, analytical feedback and decision-making."""
    
    def __init__(self):
        """Initialize logic agent."""
        pass
    
    def analyze_progress(
        self,
        apps_sent: int,
        apps_target: int,
        leetcode_done: bool,
        leetcode_target: int,
        completion_rate: float
    ) -> Dict[str, any]:
        """Analyze user progress and provide rational insights.
        
        Args:
            apps_sent: Number of applications sent
            apps_target: Target number of applications
            leetcode_done: Whether LeetCode was completed
            leetcode_target: Target number of LeetCode problems
            completion_rate: Overall completion rate (0.0-1.0)
            
        Returns:
            Analysis dictionary with insights and recommendations.
        """
        analysis = {
            "apps_completion": apps_sent / apps_target if apps_target > 0 else 0.0,
            "leetcode_completion": 1.0 if leetcode_done else 0.0,
            "overall_completion": completion_rate,
            "insights": [],
            "recommendations": [],
        }
        
        # Applications analysis
        if apps_sent >= apps_target:
            analysis["insights"].append("Application target met. Good consistency.")
        elif apps_sent > 0:
            analysis["insights"].append(f"Partial completion: {apps_sent}/{apps_target} applications.")
            analysis["recommendations"].append("Consider breaking down applications into smaller tasks.")
        else:
            analysis["insights"].append("No applications sent today.")
            analysis["recommendations"].append("Start with just one application tomorrow to build momentum.")
        
        # LeetCode analysis
        if leetcode_target > 0:
            if leetcode_done:
                analysis["insights"].append("LeetCode practice completed. Technical skills improving.")
            else:
                analysis["insights"].append("LeetCode practice skipped.")
                analysis["recommendations"].append("Start with easier problems to reduce resistance.")
        
        # Overall analysis
        if completion_rate >= 0.8:
            analysis["insights"].append("Strong completion rate. Maintain this momentum.")
        elif completion_rate >= 0.5:
            analysis["insights"].append("Moderate completion rate. Room for improvement.")
            analysis["recommendations"].append("Focus on one area at a time rather than both simultaneously.")
        else:
            analysis["insights"].append("Low completion rate. Need to adjust strategy.")
            analysis["recommendations"].append("Consider reducing daily targets to build sustainable habits.")
        
        return analysis
    
    def speak(self, analysis: Dict[str, any], max_words: int = 30) -> str:
        """Generate rational analysis message.
        
        Args:
            analysis: Analysis dictionary from analyze_progress
            max_words: Maximum words in message
            
        Returns:
            Rational analysis message.
        """
        insights = analysis.get("insights", [])
        if insights:
            # Combine insights into a message
            message = " ".join(insights[:2])  # Limit to first 2 insights
            words = message.split()
            if len(words) > max_words:
                message = " ".join(words[:max_words])
            return message
        
        return "Progress analyzed. Continue with current strategy."


# Global logic agent instance
logic_agent = LogicAgent()
