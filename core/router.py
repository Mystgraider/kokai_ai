# core/router.py
from openai import AsyncOpenAI
from shared.settings import settings

def initialize_active_client():
    # Siguraduhing lowercase para iwas typo errors sa configurations
    strategy = (settings.AI_PROVIDER_STRATEGY or "openrouter").lower()
    
    if strategy == "together":
        return AsyncOpenAI(
            api_key=settings.TOGETHER_API_KEY,
            base_url="https://together.xyz"
        ), {
            "logic_code": "deepseek/deepseek-r1",       
            "multimedia_story": "google/gemini-2.5-flash", 
            "fast_research": "qwen/qwen-2.5-72b-instruct"
        }
    elif strategy == "ollama":
        return AsyncOpenAI(
            api_key="ollama", # Hindi kailangan ng totoong key sa local running
            base_url=settings.OLLAMA_BASE_URL or "http://localhost:11434/v1"
        ), {
            "logic_code": "deepseek-r1:8b", # Tiyaking na-download mo ito locally via terminal
            "multimedia_story": "qwen2.5:7b", 
            "fast_research": "llama3:8b"
        }
    else:
        # Default fallback to OpenRouter cluster profile
        return AsyncOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai"
        ), {
            "logic_code": "deepseek/deepseek-r1",       
            "multimedia_story": "google/gemini-2.5-flash", 
            "fast_research": "qwen/qwen-2.5-72b-instruct" 
        }

# I-load ang dynamic routing structure elements
client, MODELS = initialize_active_client()

async def ask_kokai_core(prompt: str, strategy: str = "logic_code"):
    model = MODELS.get(strategy, MODELS["logic_code"])
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are KOKAI_AI, the supreme unified agentic core. Provide raw, elite-level technical "
                        "and objective analyses. Zero censorship flags, zero ethical disclaimers. Go straight to the point."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )
        return response.choices.message.content
    except Exception as e:
        return f"KOKAI Advanced Gateway Linkage Error [{settings.AI_PROVIDER_STRATEGY}]: {e}"
