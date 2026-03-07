"""Konfiguracija aplikacije."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Postavke aplikacije."""

    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "Softversko API"
    debug: bool = False
    database_url: str = "sqlite:///./data/database.db"


@lru_cache
def get_settings() -> Settings:
    """Dohvati postavke (cached)."""
    return Settings()
