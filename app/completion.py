import os

import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")


def get_completion(model_id, prompt):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = httpx.post(OPENROUTER_CHAT_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    if "choices" not in data:
        error_message = data.get("error", {}).get("message", "Unknown error from OpenRouter")
        raise RuntimeError(f"OpenRouter returned no completion for {model_id}: {error_message}")

    answer = data["choices"][0]["message"]["content"]
    usage = data["usage"]

    return {
        "answer": answer,
        "prompt_tokens": usage["prompt_tokens"],
        "completion_tokens": usage["completion_tokens"],
    }
