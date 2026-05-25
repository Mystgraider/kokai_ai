# shared/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str = ""
    TAVILY_API_KEY: str = ""
    PEXELS_API_KEY: str = ""
    YOUTUBE_CLIENT_SECRETS: str = "" 
    
    # Mga kailangang variables para sa multi-provider network links mo
    TOGETHER_API_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://localhost:11434/v1"
    AI_PROVIDER_STRATEGY: str = "openrouter" # Ito ang nawawala kaya nag-error!

    class Config:
        env_file = ".env"

settings = Settings()
