import os
import time
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="KOKAI_AI")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# RATE LIMIT
# =========================
RATE_LIMIT_STORE = {}
MAX_REQUESTS_PER_MINUTE = 15

@app.middleware("http")
async def secure_gateway_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    current_time = time.time()

    if client_ip not in RATE_LIMIT_STORE:
        RATE_LIMIT_STORE[client_ip] = []

    RATE_LIMIT_STORE[client_ip] = [
        t for t in RATE_LIMIT_STORE[client_ip]
        if current_time - t < 60
    ]

    if len(RATE_LIMIT_STORE[client_ip]) >= MAX_REQUESTS_PER_MINUTE:
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded. Try again later."}
        )

    RATE_LIMIT_STORE[client_ip].append(current_time)
    response = await call_next(request)
    return response

# =========================
# REQUEST MODEL
# =========================
class RequestBody(BaseModel):
    prompt: str

# =========================
# HOME
# =========================
@app.get("/")
async def root():
    return {
        "status": "KOKAI_AI ONLINE",
        "message": "Render deployment successful"
    }

# =========================
# CHAT
# =========================
@app.post("/chat")
async def chat(body: RequestBody):
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    if not OPENROUTER_API_KEY:
        return JSONResponse(
            status_code=500,
            content={"error": "OPENROUTER_API_KEY is not set on the server."}
        )

    # ✅ Updated May 2026 — currently active free models on OpenRouter
    MODELS = [
        "openrouter/auto",                          # Auto-selects best available free model
        "meta-llama/llama-4-maverick:free",         # Meta Llama 4 Maverick
        "meta-llama/llama-4-scout:free",            # Meta Llama 4 Scout
        "deepseek/deepseek-r1:free",                # DeepSeek R1 (reasoning)
        "deepseek/deepseek-v3-base:free",           # DeepSeek V3
        "mistralai/mistral-small-3.1-24b-instruct:free",  # Mistral Small
        "nvidia/llama-3.1-nemotron-nano-8b-v1:free" # Nvidia Nemotron
    ]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://kokai-ai.onrender.com",
        "X-Title": "KOKAI_AI"
    }

    last_error = ""
    for model in MODELS:
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": body.prompt
                        }
                    ]
                },
                timeout=60
            )
            data = response.json()
            if "choices" in data:
                ai_response = data["choices"][0]["message"]["content"]
                return {
                    "response": ai_response,
                    "model_used": model
                }
            last_error = str(data)
        except Exception as e:
            last_error = str(e)
            continue

    return JSONResponse(
        status_code=502,
        content={"error": f"All models failed. Last error: {last_error}"}
    )
