import json
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
headers = {"Authorization": f"Bearer {API_KEY}"}

payload = {
    "model": "tencent/hy3:free",
    "messages": [{"role": "user", "content": "Say hello in exactly 5 words."}],
    "reasoning": {"enabled": False},
}

response = httpx.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    json=payload,
    timeout=60,
)
response.raise_for_status()

print(json.dumps(response.json(), indent=2))
