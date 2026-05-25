from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str = ""
    TAVILY_API_KEY: str = ""
    PEXELS_API_KEY: str = ""
    YOUTUBE_CLIENT_SECRETS: str = "" 
    FACEBOOK_PAGE_ID: str = ""
    FACEBOOK_ACCESS_TOKEN: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
