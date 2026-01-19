"""Sadness agent for concerned but motivating feedback."""
from typing import List, Optional
import random


class SadnessAgent:
    """Handles concerned but motivating feedback messages."""
    
    def __init__(self):
        """Initialize sadness agent."""
        self.messages = [
            "We missed the application target. Let's try harder tomorrow.",
            "We skipped the code... again. We can't pass technical interviews like this.",
            "Target not met. Every day counts in this job search.",
            "We didn't hit our goal today. But tomorrow is a new opportunity.",
            "Missed the mark. Remember why we're doing this - we need to stay consistent.",
            "We fell short today. Let's get back on track tomorrow.",
            "No coding practice today. Technical interviews require consistent preparation.",
            "Applications missed. Every day we delay is a day we're not closer to our goal.",
        ]
    
    def speak(self, context: Optional[str] = None, max_words: int = 20) -> str:
        """Generate concerned but motivating feedback message.
        
        Args:
            context: Optional context (e.g., "applications", "leetcode")
            max_words: Maximum words in message (default: 20)
            
        Returns:
            Concerned but motivating message (short and direct).
        """
        if context:
            # Context-specific messages
            if "application" in context.lower() or "job" in context.lower():
                messages = [
                    "We missed the application target. Let's try harder tomorrow.",
                    "Target not met. Every day counts in this job search.",
                    "We didn't hit our goal today. But tomorrow is a new opportunity.",
                    "Applications missed. Every day we delay is a day we're not closer to our goal.",
                ]
            elif "leetcode" in context.lower() or "code" in context.lower():
                messages = [
                    "We skipped the code... again. We can't pass technical interviews like this.",
                    "No coding practice today. Technical interviews require consistent preparation.",
                    "LeetCode not done. We need to build our problem-solving skills.",
                    "Coding skipped. We can't improve without practice.",
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


# Global sadness agent instance
sadness_agent = SadnessAgent()
