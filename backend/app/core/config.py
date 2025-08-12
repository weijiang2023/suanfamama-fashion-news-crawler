import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_name: str = "backend"
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))

    # CORS
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")

    # Supabase
    supabase_url: Optional[str] = os.getenv("SUPABASE_URL")
    supabase_anon_key: Optional[str] = os.getenv("SUPABASE_ANON_KEY")

    # Direct Postgres (Supabase DB)
    supabase_db_url: Optional[str] = os.getenv("SUPABASE_DB_URL")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()