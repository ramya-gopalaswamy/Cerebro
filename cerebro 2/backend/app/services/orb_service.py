"""Orb generation service for tracking user progress."""
from typing import Dict, Tuple
from datetime import datetime
from app.models.user import OrbInventory


class OrbService:
    """Handles orb generation and tracking."""
    
    # Orb types
    GOLD = "gold"  # Success - target met
    BLUE = "blue"  # Missed - target not met
    RED = "red"    # Critical - multiple consecutive misses
    
    def __init__(self):
        """Initialize orb service."""
        pass
    
    def generate_orbs(
        self,
        apps_sent: int,
        apps_target: int,
        leetcode_done: bool,
        leetcode_target: int
    ) -> Tuple[Dict[str, int], Dict[str, str]]:
        """Generate orbs based on verification results.
        
        Args:
            apps_sent: Number of job applications sent
            apps_target: Target number of applications
            leetcode_done: Whether LeetCode problem was completed
            leetcode_target: Target number of LeetCode problems
            
        Returns:
            Tuple of (orbs_dict, messages_dict)
            - orbs_dict: {"gold": count, "blue": count, "red": count}
            - messages_dict: {"gold": message, "blue": message, "red": message}
        """
        orbs = {"gold": 0, "blue": 0, "red": 0}
        messages = {}
        
        # Check applications
        if apps_sent >= apps_target:
            orbs["gold"] += 1
            messages["gold"] = f"Applications sent! Great work hitting the quota ({apps_sent}/{apps_target})."
        else:
            orbs["blue"] += 1
            messages["blue"] = f"We missed the application target ({apps_sent}/{apps_target}). Let's try harder tomorrow."
        
        # Check LeetCode
        if leetcode_target > 0:
            if leetcode_done:
                orbs["gold"] += 1
                if "gold" in messages:
                    messages["gold"] += " LeetCode completed! Keep coding."
                else:
                    messages["gold"] = "LeetCode problem solved! Great work."
            else:
                orbs["blue"] += 1
                if "blue" in messages:
                    messages["blue"] += " We skipped the code... again. We can't pass technical interviews like this."
                else:
                    messages["blue"] = "We skipped the code... again. We can't pass technical interviews like this."
        
        # Note: Red orbs would be generated based on consecutive misses
        # This logic would be in the verification endpoint
        
        return orbs, messages
    
    def add_orbs_to_inventory(
        self,
        current_inventory: Dict[str, int],
        new_orbs: Dict[str, int]
    ) -> Dict[str, int]:
        """Add new orbs to existing inventory.
        
        Args:
            current_inventory: Current orb counts
            new_orbs: New orbs to add
            
        Returns:
            Updated inventory dictionary.
        """
        updated = {
            "gold": current_inventory.get("gold", 0) + new_orbs.get("gold", 0),
            "blue": current_inventory.get("blue", 0) + new_orbs.get("blue", 0),
            "red": current_inventory.get("red", 0) + new_orbs.get("red", 0),
        }
        return updated
    
    def get_orb_summary(self, inventory: Dict[str, int]) -> Dict[str, any]:
        """Get summary of orb inventory.
        
        Args:
            inventory: Orb inventory dictionary
            
        Returns:
            Summary dictionary with counts and total.
        """
        total = sum(inventory.values())
        return {
            "gold": inventory.get("gold", 0),
            "blue": inventory.get("blue", 0),
            "red": inventory.get("red", 0),
            "total": total,
        }


# Global orb service instance
orb_service = OrbService()
