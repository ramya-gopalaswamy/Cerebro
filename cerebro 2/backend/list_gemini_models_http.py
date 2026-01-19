import os
import requests
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
url = "https://generativelanguage.googleapis.com/v1/models?key=" + api_key
headers = {"Content-Type": "application/json"}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    models = response.json().get("models", [])
    print("Available Gemini models:")
    for m in models:
        print(f"Name: {m['name']}")
        print(f"  Supported generation methods: {m.get('supportedGenerationMethods', [])}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
