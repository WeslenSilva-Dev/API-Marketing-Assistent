"""
Configurações da aplicação via variáveis de ambiente.
"""
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Pasta do projeto (onde está main.py) para carregar .env sempre do mesmo lugar
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = ROOT_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH) if ENV_PATH.exists() else ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # OpenAI (DALL-E + ChatGPT)
    openai_api_key: str = ""

    @field_validator("openai_api_key")
    @classmethod
    def strip_api_key(cls, v: str) -> str:
        return (v or "").strip()

    # Facebook Graph API / Instagram
    ig_user_id: Optional[str] = None
    facebook_app_id: Optional[str] = None
    facebook_app_secret: Optional[str] = None
    user_access_token: Optional[str] = None

    # App
    app_name: str = "Instagram Content API"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
