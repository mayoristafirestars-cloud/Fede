"""Configuración cargada desde variables de entorno (.env)."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Meta
    meta_access_token: str = ""
    meta_verify_token: str = "cambiame"
    meta_app_secret: str = ""
    whatsapp_phone_number_id: str = ""
    instagram_account_id: str = ""

    # Anthropic
    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-5"

    # OpenAI (Whisper)
    openai_api_key: str = ""
    whisper_model: str = "whisper-1"

    # Google Sheets
    google_service_account_json: str = ""
    google_service_account_file: str = ""
    google_sheet_id: str = ""
    google_sheet_tab: str = "Precios"
    sheet_cache_seconds: int = 300

    # Negocio
    business_name: str = "Mi Negocio"
    business_timezone: str = "America/Argentina/Buenos_Aires"

    # Persistencia
    conversations_db: str = "data/conversations.db"

    # Server
    port: int = 8000


@lru_cache
def get_settings() -> Settings:
    s = Settings()
    # Asegurar que el directorio de la base de datos exista.
    db_path = Path(s.conversations_db)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return s
