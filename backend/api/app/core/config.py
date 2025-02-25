from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://scribex:devpassword@db:5432/scribex_db"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ScribeX"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    class Config:
        env_file = ".env"

settings = Settings() 