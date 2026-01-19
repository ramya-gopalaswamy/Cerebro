import os
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

JOURNAL_DATA_PATH = os.path.join(os.path.dirname(__file__), "journal_demo_data.json")

def aggregate_journal_stats(journal):
    # Load user targets from user_profile.json
    user_profile_path = os.path.join(os.path.dirname(__file__), "user_profile.json")
    if os.path.exists(user_profile_path):
        with open(user_profile_path) as f:
            user_profile = json.load(f)
        target_apps = user_profile.get("target_apps", 5)
        target_leetcode = user_profile.get("target_leetcode", 5)
    else:
        target_apps = 5
        target_leetcode = 5
    total_apps = 0
    total_leetcode = 0
    easy_solved = 0
    medium_solved = 0
    hard_solved = 0
    easy_suggested = 0
    medium_suggested = 0
    hard_suggested = 0
    skipped_days = []
    day_names = []
    for entry in journal:
        total_apps += entry.get("applications", 0)
        leet_solved = entry.get("leetcode_solved", entry.get("leetcode", {}))
        leet_suggested = entry.get("leetcode_suggested", entry.get("leetcode", {}))
        easy_solved += leet_solved.get("easy", 0)
        medium_solved += leet_solved.get("medium", 0)
        hard_solved += leet_solved.get("hard", 0)
        easy_suggested += leet_suggested.get("easy", 0)
        medium_suggested += leet_suggested.get("medium", 0)
        hard_suggested += leet_suggested.get("hard", 0)
        total_leetcode += sum([leet_solved.get("easy", 0), leet_solved.get("medium", 0), leet_solved.get("hard", 0)])
        if entry.get("applications", 0) == 0 and total_leetcode == 0:
            skipped_days.append(entry.get("date", ""))
        day_names.append(entry.get("date", ""))
    return {
        "total_apps": total_apps,
        "total_leetcode": total_leetcode,
        "easy_solved": easy_solved,
        "medium_solved": medium_solved,
        "hard_solved": hard_solved,
        "easy_suggested": easy_suggested,
        "medium_suggested": medium_suggested,
        "hard_suggested": hard_suggested,
        "skipped_days": skipped_days,
        "all_days": day_names,
        "target_apps": target_apps,
        "target_leetcode": target_leetcode
    }

def build_prompt(stats):
    prompt = f'''
The Scenario Stats:
Applications: {stats['total_apps']} sent (Target was {stats['target_apps']})
Coding: {stats['total_leetcode']} problems solved (Target was {stats['target_leetcode']})
Difficulty: {stats['easy_solved']}/{stats['easy_suggested']} 'Easy', {stats['medium_solved']}/{stats['medium_suggested']} 'Medium', {stats['hard_solved']}/{stats['hard_suggested']} 'Hard'.
Consistency: You completely skipped {len(stats['skipped_days'])} days ({', '.join(stats['skipped_days']) if stats['skipped_days'] else 'None'}).

Scene: A boardroom inside your mind. The five emotional agents are sitting around a table: LOGIC (Cyan), ANXIETY (Purple), ANGER (Red), SADNESS (Blue), JOY (Yellow).

Write a conversation between ANXIETY, ANGER, SADNESS, JOY, and LOGIC, each with their own perspective on the week, referencing the stats above. End with LOGIC giving a summary and directive for next week.

Keep each agent's comment short and direct (1-2 sentences max).

Format as dialogue, with each agent's name in ALL CAPS, a colon, and their speech. Example:
LOGIC: Here is my logical analysis.
JOY: (beaming) That sounds great!
SADNESS: (sighs) I wish it were better.
ANGER: (fuming) This is not enough!
ANXIETY: (nervous) What if we fail?

Now, write the conversation:
'''
    return prompt

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

def call_claude(prompt):
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": "claude-3-haiku-20240307",  # updated model name for broadest access
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        try:
            return result["content"][0]["text"]
        except Exception as e:
            print("[ERROR] Claude response parsing failed:", e)
            return None
    else:
        print("[ERROR] Claude API call failed:", response.status_code, response.text)
        return None

@router.get("/api/journal/summary")
def get_journal_summary():
    if not os.path.exists(JOURNAL_DATA_PATH):
        raise HTTPException(status_code=404, detail="Journal data not found.")
    with open(JOURNAL_DATA_PATH, "r") as f:
        journal = json.load(f)
    stats = aggregate_journal_stats(journal)
    prompt = build_prompt(stats)
    summary = call_claude(prompt)
    if not summary:
        summary = "LOGIC: (calmly) Unable to generate a summary this week due to a technical issue with Claude API."
    return JSONResponse(content={"summary": summary, "stats": stats})
