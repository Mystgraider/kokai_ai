import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

SYSTEM_PROMPT = """
You are KOKAI_AI.

An advanced autonomous AI reasoning system with:
- Deep analysis
- Coding support
- Security intelligence
- Research capabilities
- Professional responses
"""

async def run_autonomous_kokai_loop(prompt: str):

    try:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://kokai-ai.onrender.com",
                "X-Title": "KOKAI_AI"
            },
            json={
                "model": "deepseek/deepseek-r1:free",
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 800
            },
            timeout=60
        )

        print("STATUS:", response.status_code)
        print("RAW:", response.text)

        data = response.json()

        # SAFE PARSE

        if "choices" in data:

            message = data["choices"][0]["message"]["content"]

            if not message:
                return "KOKAI_AI received empty response."

            return message

        # ERROR HANDLING

        if "error" in data:
            return f"KOKAI_AI Gateway Error: {data['error']}"

        return str(data)

    except Exception as e:

        return f"KOKAI_AI Advanced Gateway Linkage Error [openrouter]: {str(e)}"
