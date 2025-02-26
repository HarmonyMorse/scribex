from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path
import os

class Settings(BaseSettings):
    # Base
    ENV: str = "development"
    ENV_FILE: str = str(Path(__file__).parent.parent.parent / ".env")
    DEBUG: bool = True
    
    # Database
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./app.db"
    DATABASE_URL: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key"  # Change in production
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]
    
    # External APIs
    OPENAI_API_KEY: Optional[str] = None
    SAPLING_API_KEY: Optional[str] = None
    WHISPER_API_KEY: Optional[str] = None

    class Config:
        env_file = os.getenv("ENV_FILE", ".env")
        case_sensitive = True

settings = Settings() 