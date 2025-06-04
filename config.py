"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Main settings object."""

    BOT_TOKEN: str = "token"
    DATABASE_URL: str = "sqlite:///./test.db"
    ADMIN_CHAT_ID: int = 0
    REDIS_URL: str | None = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
