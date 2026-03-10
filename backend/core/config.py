"""
core/config.py
--------------
Application settings loaded from environment variables via Pydantic BaseSettings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central configuration – reads from .env or OS environment."""

    # ── Database ──────────────────────────────────────────
    # Production: set DATABASE_URL=postgresql://rakshita_user:rakshita_pass@localhost:5432/rakshita_db
    # Local dev default: SQLite (no PostgreSQL install required)
    DATABASE_URL: str = "sqlite:///./rakshita_dev.db"

    # ── JWT / Auth ────────────────────────────────────────
    JWT_SECRET_KEY: str = "CHANGE-ME-IN-PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ── App Metadata ──────────────────────────────────────
    APP_NAME: str = "Rakshita – Smart Civic Grievance Engine"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
