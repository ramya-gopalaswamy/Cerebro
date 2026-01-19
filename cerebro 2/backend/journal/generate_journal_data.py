import json
import random
import os
from datetime import datetime, timedelta

# --- CONFIGURATION ---
START_DATE = datetime.now() - timedelta(days=7)

# Load user profile
user_profile_path = os.path.join(os.path.dirname(__file__), "user_profile.json")
with open(user_profile_path) as f:
    user_profile = json.load(f)
USER_ROLE = user_profile.get("role", "Frontend Developer")
DAILY_GOAL_LEETCODE = user_profile.get("target_leetcode", 5)
DAILY_GOAL_APPS = user_profile.get("target_apps", 5)

LEETCODE_PROBLEMS = [
    {"title": "Two Sum", "difficulty": "Easy"},
    {"title": "Invert Binary Tree", "difficulty": "Easy"},
    {"title": "LRU Cache", "difficulty": "Medium"},
    {"title": "Merge K Sorted Lists", "difficulty": "Hard"},
    {"title": "Valid Parentheses", "difficulty": "Easy"},
    {"title": "Trapping Rain Water", "difficulty": "Hard"},
    {"title": "Group Anagrams", "difficulty": "Medium"},
    {"title": "Longest Substring Without Repeating Characters", "difficulty": "Medium"},
    {"title": "Median of Two Sorted Arrays", "difficulty": "Hard"},
    {"title": "Add Two Numbers", "difficulty": "Medium"},
    {"title": "Valid Anagram", "difficulty": "Easy"},
    {"title": "Maximum Subarray", "difficulty": "Easy"},
    {"title": "Container With Most Water", "difficulty": "Medium"},
    {"title": "Climbing Stairs", "difficulty": "Easy"},
    {"title": "Best Time to Buy and Sell Stock", "difficulty": "Easy"},
    {"title": "Valid Palindrome", "difficulty": "Easy"},
    {"title": "Linked List Cycle", "difficulty": "Easy"}
]

COMPANIES = ["Vercel", "Google", "Netflix", "Linear", "Stripe", "Amazon", "Meta", "Shopify", "TechCorp", "InnovateX", "Webify", "DataWiz", "PixelPush", "Testify", "Cloudify", "Appify", "NetSecure", "HelpDeskPro"]


def generate_week_data():
    # Distribute exactly 7 applications and 4 leetcode problems
    app_distribution = [2, 1, 1, 1, 1, 1, 0]  # sum = 7
    leet_distribution = [1, 1, 1, 1, 0, 0, 0] # sum = 4
    history = []
    for i in range(7):
        current_date = START_DATE + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        day_log = {
            "date": date_str,
            "day_name": current_date.strftime("%A"),
            "target": {"apps": DAILY_GOAL_APPS, "leetcode": DAILY_GOAL_LEETCODE},
            "actual": {"apps": app_distribution[i], "leetcode": []},
            "mood": random.choice(["JOY", "LOGIC", "ANXIETY", "SADNESS", "ANGER"])
        }
        if leet_distribution[i] > 0:
            day_log["actual"]["leetcode"] = random.sample(LEETCODE_PROBLEMS, k=leet_distribution[i])
        # Job details
        job_details = []
        if day_log["actual"]["apps"] > 0:
            targets = random.sample(COMPANIES, k=day_log["actual"]["apps"])
            for company in targets:
                job_details.append({
                    "role": USER_ROLE,
                    "company": company,
                    "platform": "LinkedIn",
                    "status": "applied"
                })
        day_log["job_details"] = job_details
        history.append(day_log)
    with open("journal_demo_data.json", "w") as f:
        json.dump(history, f, indent=2)
    print("✅ Demo journal data generated: 7 applications, 4 leetcode problems.")

if __name__ == "__main__":
    generate_week_data()
