# config.py
from pydantic_settings import BaseSettings
from pydantic import field_validator
import secrets


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Team Task Manager"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite:///./taskmanager.db"

    # JWT
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
