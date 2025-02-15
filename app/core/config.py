from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "Terranova IA"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Plateforme d'intelligence artificielle multi-services"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    SECRET_KEY: str
    ALLOWED_HOSTS: List[str] = ["*"]

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # AI Services
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str
    STABILITY_API_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
