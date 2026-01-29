from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Poker Hand Memorisation App"
    debug: bool = True
    database_url: str = "sqlite:///./poker_training.db"

    # Anonymous user ID for MVP (no auth)
    default_user_id: str = "anonymous"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
