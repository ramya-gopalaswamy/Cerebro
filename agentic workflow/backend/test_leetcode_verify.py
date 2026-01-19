"""
Test script for LeetCode verification using TinyFish
"""
import asyncio
import json
import os
import sys
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Set environment variable if not already set
if not os.environ.get("TINYFISH_API_KEY"):
    raise RuntimeError("TINYFISH_API_KEY not set in environment or .env file.")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.leetcode_verifier import (
    tinyfish_leetcode_login,
    tinyfish_check_submissions,
    verify_daily_leetcode,
    LeetCodeProblem
)

async def test_verification():
    """Test the full verification flow"""
    
    # Problems from the daily plan
    test_problems = [
        {"title": "Two Sum", "difficulty": "Easy", "url": "https://leetcode.com/problems/two-sum/"},
        {"title": "Valid Parentheses", "difficulty": "Easy", "url": "https://leetcode.com/problems/valid-parentheses/"},
    ]
    
    # Test with a public profile (no login needed)
    # Replace 'neal_wu' with any public LeetCode username to test
    test_username = "neal_wu"  # Famous competitive programmer with public profile
    
    print("\n" + "="*70)
    print("🧪 TESTING LEETCODE VERIFICATION WITH TINYFISH")
    print("="*70)
    print(f"\n📌 Username: {test_username}")
    print(f"📌 Problems to verify: {len(test_problems)}")
    for p in test_problems:
        print(f"   - {p['title']} ({p['difficulty']})")
    print("\n")
    
    # Run verification (without login - public profile)
    result = await verify_daily_leetcode(
        email="",  # No login for public profile
        password="",
        username=test_username,
        problems=test_problems
    )
    
    print("\n" + "="*70)
    print("📊 FINAL RESULT")
    print("="*70)
    print(json.dumps(result, indent=2, default=str))
    
    return result


def test_submission_check_only():
    """Test just the submission check (no login, no LLM)"""
    
    test_username = "neal_wu"
    problems = [
        LeetCodeProblem(title="Two Sum", difficulty="Easy"),
        LeetCodeProblem(title="Add Two Numbers", difficulty="Medium"),
    ]
    
    print("\n" + "="*70)
    print("🧪 TESTING SUBMISSION CHECK ONLY (TinyFish)")
    print("="*70)
    print(f"Username: {test_username}")
    print(f"Checking {len(problems)} problems...")
    print()
    
    result = tinyfish_check_submissions(problems, test_username)
    
    print("\n" + "="*70)
    print("📊 RAW RESULT FROM TINYFISH")
    print("="*70)
    print(json.dumps(result, indent=2, default=str))
    
    return result


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test LeetCode verification")
    parser.add_argument("--full", action="store_true", help="Run full verification with LLM")
    parser.add_argument("--check-only", action="store_true", help="Only check submissions (no LLM)")
    parser.add_argument("--username", type=str, default="neal_wu", help="LeetCode username to check")
    
    args = parser.parse_args()
    
    if args.check_only:
        test_submission_check_only()
    else:
        asyncio.run(test_verification())
