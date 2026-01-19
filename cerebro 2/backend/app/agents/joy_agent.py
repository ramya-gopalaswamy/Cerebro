"""Joy agent for positive feedback."""
from typing import List, Optional
import random


class JoyAgent:
    """Handles positive, encouraging feedback messages."""
    
    def __init__(self):
        """Initialize joy agent."""
        self.messages = [
            "Applications sent! Great work hitting the quota.",
            "Target hit! You're on track to land that job.",
            "Excellent progress! Keep up the momentum.",
            "You did it! Consistency is key to success.",
            "Well done! Every application brings you closer.",
            "Outstanding! You're building great habits.",
            "Perfect! You're making it happen.",
            "Amazing work! Keep pushing forward.",
            "LeetCode completed! Great job solving that problem.",
            "Coding practice done! You're leveling up your skills.",
        ]
    
    def speak(self, context: Optional[str] = None, max_words: int = 20) -> str:
        """Generate positive feedback message.
        
        Args:
            context: Optional context (e.g., "applications", "leetcode")
            max_words: Maximum words in message (default: 20)
            
        Returns:
            Positive feedback message (short and punchy).
        """
        if context:
            # Context-specific messages
            if "application" in context.lower() or "job" in context.lower():
                messages = [
                    "Applications sent! Great work hitting the quota.",
                    "Target hit! You're on track to land that job.",
                    "Excellent progress! Keep up the momentum.",
                    "Well done! Every application brings you closer.",
                ]
            elif "leetcode" in context.lower() or "code" in context.lower():
                messages = [
                    "LeetCode completed! Great job solving that problem.",
                    "Coding practice done! You're leveling up your skills.",
                    "Problem solved! Keep building that interview muscle.",
                    "Code challenge conquered! Well done.",
                ]
            else:
                messages = self.messages
        else:
            messages = self.messages
        
        message = random.choice(messages)
        
        # Ensure max_words constraint
        words = message.split()
        if len(words) > max_words:
            message = " ".join(words[:max_words])
        
        return message


# Global joy agent instance
joy_agent = JoyAgent()
