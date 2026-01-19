"""LeetCode service for fetching problems."""
import requests
import random
from typing import Dict, Optional, List
from app.config import settings


class LeetCodeService:
    """Handles LeetCode problem fetching and selection."""
    
    def __init__(self):
        """Initialize LeetCode service."""
        # LeetCode GraphQL API endpoint (public, no auth required)
        self.graphql_url = "https://leetcode.com/graphql"
        # Curated problem list for fallback
        self.curated_problems = self._load_curated_problems()
    
    def get_problem(
        self,
        difficulty: Optional[str] = None,
        topic: Optional[str] = None,
        exclude_solved: bool = False
    ) -> Dict:
        """Fetch a LeetCode problem.
        
        Args:
            difficulty: Problem difficulty ("Easy", "Medium", "Hard"). If None, random.
            topic: Problem topic/tag (e.g., "Array", "String", "Dynamic Programming")
            exclude_solved: Whether to exclude solved problems (requires user profile)
            
        Returns:
            Problem dictionary with id, title, url, difficulty, topics.
            
        TODO: Implement GraphQL API call when needed.
        For now, returns from curated list.
        """
        if not difficulty:
            difficulty = random.choice(["Easy", "Medium", "Hard"])
        
        # Try to fetch from API (if implemented)
        try:
            problem = self._fetch_from_api(difficulty, topic)
            if problem:
                return problem
        except Exception as e:
            print(f"LeetCode API error: {e}")
        
        # Fallback to curated list
        return self._get_from_curated(difficulty, topic)
    
    def _fetch_from_api(self, difficulty: str, topic: Optional[str]) -> Optional[Dict]:
        """Fetch problem from LeetCode GraphQL API.
        
        Args:
            difficulty: Problem difficulty
            topic: Problem topic (optional)
            
        Returns:
            Problem dictionary or None if API fails.
            
        TODO: Implement GraphQL query for LeetCode API.
        """
        # LeetCode GraphQL query example:
        # query {
        #   problemsetQuestionList(categorySlug: "", filters: {difficulty: "Easy"}) {
        #     questions {
        #       questionId
        #       title
        #       titleSlug
        #       difficulty
        #       topicTags { name }
        #     }
        #   }
        # }
        return None
    
    def check_user_submission(
        self,
        username: Optional[str] = None,
        timeframe_hours: int = 24
    ) -> bool:
        """Check if user has submitted a LeetCode solution recently.
        
        Args:
            username: LeetCode username (optional)
            timeframe_hours: Hours to look back (default: 24)
            
        Returns:
            True if submission found, False otherwise.
            
        TODO: Implement LeetCode profile checking.
        Options:
        1. Scrape public profile page
        2. Use LeetCode API (if available)
        3. Ask user to paste submission link (manual)
        """
        if not username:
            # For development: return mock result
            return self._get_mock_submission_status()
        
        # TODO: Implement actual checking
        # Option 1: Scrape public profile
        # Option 2: Use API
        # Option 3: Manual link submission
        
        return False
    
    def _get_mock_submission_status(self) -> bool:
        """Get mock submission status for development.
        
        Returns:
            Mock boolean (random for testing).
        """
        import random
        # For development: return random result
        # In production, this would check actual LeetCode profile
        return random.choice([True, False])
    
    def _get_from_curated(self, difficulty: str, topic: Optional[str]) -> Dict:
        """Get problem from curated list.
        
        Args:
            difficulty: Problem difficulty
            topic: Problem topic (optional)
            
        Returns:
            Problem dictionary.
        """
        # Filter by difficulty
        filtered = [p for p in self.curated_problems if p["difficulty"] == difficulty]
        
        if not filtered:
            # If no match, return any problem
            filtered = self.curated_problems
        
        # Filter by topic if specified
        if topic:
            topic_filtered = [p for p in filtered if topic in p.get("topics", [])]
            if topic_filtered:
                filtered = topic_filtered
        
        # Return random problem from filtered list
        problem = random.choice(filtered)
        
        return {
            "id": problem["id"],
            "title": problem["title"],
            "url": f"https://leetcode.com/problems/{problem['slug']}/",
            "difficulty": problem["difficulty"],
            "topics": problem.get("topics", []),
            "description": problem.get("description", ""),
        }
    
    def _load_curated_problems(self) -> List[Dict]:
        """Load curated list of LeetCode problems.
        
        Returns:
            List of problem dictionaries.
        """
        return [
            # Easy problems
            {
                "id": "1",
                "slug": "two-sum",
                "title": "Two Sum",
                "difficulty": "Easy",
                "topics": ["Array", "Hash Table"],
                "description": "Given an array of integers, return indices of the two numbers that add up to target.",
            },
            {
                "id": "20",
                "slug": "valid-parentheses",
                "title": "Valid Parentheses",
                "difficulty": "Easy",
                "topics": ["String", "Stack"],
                "description": "Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
            },
            {
                "id": "121",
                "slug": "best-time-to-buy-and-sell-stock",
                "title": "Best Time to Buy and Sell Stock",
                "difficulty": "Easy",
                "topics": ["Array", "Dynamic Programming"],
                "description": "Find the maximum profit you can achieve by buying and selling a stock once.",
            },
            {
                "id": "217",
                "slug": "contains-duplicate",
                "title": "Contains Duplicate",
                "difficulty": "Easy",
                "topics": ["Array", "Hash Table"],
                "description": "Given an integer array nums, return true if any value appears at least twice.",
            },
            {
                "id": "53",
                "slug": "maximum-subarray",
                "title": "Maximum Subarray",
                "difficulty": "Easy",
                "topics": ["Array", "Dynamic Programming", "Divide and Conquer"],
                "description": "Find the contiguous subarray with the largest sum.",
            },
            # Medium problems
            {
                "id": "2",
                "slug": "add-two-numbers",
                "title": "Add Two Numbers",
                "difficulty": "Medium",
                "topics": ["Linked List", "Math", "Recursion"],
                "description": "You are given two non-empty linked lists representing two non-negative integers.",
            },
            {
                "id": "3",
                "slug": "longest-substring-without-repeating-characters",
                "title": "Longest Substring Without Repeating Characters",
                "difficulty": "Medium",
                "topics": ["String", "Hash Table", "Sliding Window"],
                "description": "Find the length of the longest substring without repeating characters.",
            },
            {
                "id": "15",
                "slug": "3sum",
                "title": "3Sum",
                "difficulty": "Medium",
                "topics": ["Array", "Two Pointers", "Sorting"],
                "description": "Find all unique triplets in the array which gives the sum of zero.",
            },
            {
                "id": "22",
                "slug": "generate-parentheses",
                "title": "Generate Parentheses",
                "difficulty": "Medium",
                "topics": ["String", "Backtracking", "Dynamic Programming"],
                "description": "Given n pairs of parentheses, generate all combinations of well-formed parentheses.",
            },
            {
                "id": "46",
                "slug": "permutations",
                "title": "Permutations",
                "difficulty": "Medium",
                "topics": ["Array", "Backtracking"],
                "description": "Given an array of distinct integers, return all the possible permutations.",
            },
            # Hard problems
            {
                "id": "4",
                "slug": "median-of-two-sorted-arrays",
                "title": "Median of Two Sorted Arrays",
                "difficulty": "Hard",
                "topics": ["Array", "Binary Search", "Divide and Conquer"],
                "description": "Find the median of the two sorted arrays.",
            },
            {
                "id": "23",
                "slug": "merge-k-sorted-lists",
                "title": "Merge k Sorted Lists",
                "difficulty": "Hard",
                "topics": ["Linked List", "Divide and Conquer", "Heap"],
                "description": "Merge k sorted linked lists and return it as one sorted list.",
            },
            {
                "id": "32",
                "slug": "longest-valid-parentheses",
                "title": "Longest Valid Parentheses",
                "difficulty": "Hard",
                "topics": ["String", "Dynamic Programming", "Stack"],
                "description": "Find the length of the longest valid parentheses substring.",
            },
        ]


# Global LeetCode service instance
leetcode_service = LeetCodeService()
