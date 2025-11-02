from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # FastAPI application settings
    app_name: str = "SmartSense Inbox"
    api_version: str = "v1"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    # Database settings
    database_url: str = "sqlite:///./sms.db"

    # LLM API Key (OpenRouter/OpenAI)
    openai_api_key: Optional[str] = None  # Also used for OpenRouter

    # Ngrok URL (for forwarder configuration)
    ngrok_url: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()