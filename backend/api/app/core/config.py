from pydantic_settings import BaseSettings
from pathlib import Path
from os import getenv

class Settings(BaseSettings):
    DATABASE_URL: str = f"postgresql://scribex:{getenv('POSTGRES_PASSWORD')}@db:5432/{getenv('POSTGRES_DB')}"
    PROJECT_NAME: str = "ScribeX"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    OPENAI_API_KEY: str = getenv('OPENAI_API_KEY')
    SAPLING_API_KEY: str = getenv('SAPLING_API_KEY')
    WHISPER_API_KEY: str = getenv('WHISPER_API_KEY')
    POSTGRES_USER: str = getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: str = getenv('POSTGRES_PASSWORD')
    POSTGRES_DB: str = getenv('POSTGRES_DB')
    class Config:
        env_file = "/app/.env"

settings = Settings() 