import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def run_autonomous_kokai_loop(prompt: str):

    try:

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://kokai-ai.onrender.com",
                "X-Title": "KOKAI_AI"
            },
            json={
                "model": "google/gemma-3-27b-it:free",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are KOKAI_AI, an advanced autonomous AI assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=60
        )

        print("STATUS:", response.status_code)
        print("TEXT:", response.text)

        # SAFE JSON CHECK

        try:
            data = response.json()
        except Exception:
            return f"INVALID RESPONSE:\n\n{response.text}"

        # SUCCESS

        if "choices" in data:

            return data["choices"][0]["message"]["content"]

        # API ERROR

        if "error" in data:

            return f"OPENROUTER ERROR:\n\n{data['error']}"

        return str(data)

    except Exception as e:

        return f"SYSTEM FAILURE:\n\n{str(e)}"
