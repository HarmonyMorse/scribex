from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

class Settings(BaseSettings):
    """Application settings"""
    PROJECT_NAME: str = "ScribeX API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # JWT Settings
    JWT_SECRET_KEY: str = "your-secret-key-here"  # Change in production!
    JWT_REFRESH_SECRET_KEY: str = "your-refresh-secret-key-here"  # Change in production!
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "test_openai_key_123")
    SAPLING_API_KEY: str = os.getenv("SAPLING_API_KEY", "test_sapling_key_123")
    WHISPER_API_KEY: str = os.getenv("WHISPER_API_KEY", "test_whisper_key_123")
    
    # Database settings
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "test_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "test_password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "test_db")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://test_user:test_password@localhost:5432/test_db"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env.test" if os.getenv("TESTING") else "/app/.env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings() 