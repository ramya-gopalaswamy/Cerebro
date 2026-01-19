import os
import requests
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
FREEPIK_API_KEY = os.getenv("FREEPIK_API_KEY")
FREEPIK_API_URL = "https://api.freepik.com/v1/resources"

@router.get("/api/motivation-image")
def get_motivation_image(query: str = Query("motivation")):
    headers = {"Accept": "application/json", "Authorization": f"Bearer {FREEPIK_API_KEY}"}
    params = {"term": query, "limit": 1, "type": "photo"}
    resp = requests.get(FREEPIK_API_URL, headers=headers, params=params)
    if resp.status_code == 200:
        data = resp.json()
        if data.get("data"):
            image_url = data["data"][0]["assets"]["preview"]["url"]
            title = data["data"][0].get("title", "Motivation")
            return JSONResponse(content={"image_url": image_url, "title": title})
        else:
            return JSONResponse(content={"image_url": None, "title": "No image found."})
    else:
        return JSONResponse(content={"image_url": None, "title": "Freepik API error."}, status_code=500)
