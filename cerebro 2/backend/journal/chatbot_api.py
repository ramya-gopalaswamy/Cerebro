from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import os
import requests
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

# Map keywords to agents
AGENT_KEYWORDS = {
    "sad": "SADNESS",
    "depress": "SADNESS",
    "unhappy": "SADNESS",
    "motivat": "SADNESS",
    "anx": "ANXIETY",
    "worr": "ANXIETY",
    "stress": "ANXIETY",
    "panic": "ANXIETY",
    "angry": "ANGER",
    "mad": "ANGER",
    "frustrat": "ANGER",
    "logic": "LOGIC",
    "plan": "LOGIC",
    "think": "LOGIC",
    "happy": "JOY",
    "joy": "JOY",
    "excite": "JOY",
    "good": "JOY",
    "ok": "JOY",
    "fine": "JOY",
}

AGENT_PERSONAS = {
    "SADNESS": "You are Sadness from Inside Out. You respond with empathy and gentle support, acknowledging the user's feelings.",
    "ANXIETY": "You are Anxiety from Inside Out. You respond with concern and caution, focusing on what could go wrong and how to prepare.",
    "ANGER": "You are Anger from Inside Out. You respond with fiery passion, frustration, or a drive to fix things quickly.",
    "JOY": "You are Joy from Inside Out. You respond with optimism, encouragement, and positive suggestions.",
    "LOGIC": "You are Logic, the rational core. You respond with calm, practical advice and clear reasoning.",
}

def pick_agent(user_message: str) -> str:
    msg = user_message.lower()
    for kw, agent in AGENT_KEYWORDS.items():
        if kw in msg:
            return agent
    # fallback: Joy for positive, Sadness for negative, Logic for neutral
    if any(w in msg for w in ["help", "how", "what", "should", "can", "do", "plan"]):
        return "LOGIC"
    if any(w in msg for w in ["sad", "depress", "unhappy", "demotivat", "tired", "down"]):
        return "SADNESS"
    if any(w in msg for w in ["anx", "worr", "panic", "stress"]):
        return "ANXIETY"
    if any(w in msg for w in ["angry", "mad", "frustrat"]):
        return "ANGER"
    return "JOY"

@router.post("/api/chatbot")
async def chatbot_endpoint(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    prompt = f"""
Scene: The Inside Out boardroom. The five agents (SADNESS, ANXIETY, ANGER, JOY, LOGIC) are present.
User: {user_message}
Each agent who feels their perspective is relevant should respond in character, in 1-2 sentences. Format as:
AGENT: (emotion) response
Only respond if your emotion is relevant. Do not break character. Do not mention other agents unless responding to them. Keep it short and conversational.
"""
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    payload = {
        "model": "claude-3-haiku-20240307",  # updated model name for broadest access
        "max_tokens": 400,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(CLAUDE_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        try:
            text = result["content"][0]["text"]
        except Exception:
            text = "Sorry, I couldn't generate a response right now."
    else:
        text = "Sorry, I couldn't connect to the LLM."
    replies = []
    for line in text.splitlines():
        if ":" in line:
            agent, msg = line.split(":", 1)
            agent = agent.strip().upper()
            msg = msg.strip()
            if agent in ["SADNESS", "ANXIETY", "ANGER", "JOY", "LOGIC"]:
                replies.append({"agent": agent, "text": msg})
    if not replies:
        replies = [{"agent": "LOGIC", "text": text}]
    return JSONResponse(content={"replies": replies})
