"""
Application settings loaded from environment variables.

See debt.txt at repository root for placeholder keys and descriptions.
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/ directory
BACKEND_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = BACKEND_ROOT.parent
DATA_DIR = BACKEND_ROOT / "data"


class Settings(BaseSettings):
    """Runtime configuration for the CanaHub API."""

    model_config = SettingsConfigDict(
        env_file=(BACKEND_ROOT / ".env", REPO_ROOT / "debt.txt"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    app_secret_key: str = "dev-secret-change-me"
    api_base_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:4200"

    database_url: str = f"sqlite:///{DATA_DIR / 'cannahub.db'}"

    author_email: str = "author@example.com"
    author_name: str = "Papi Ro Ebers"

    llm_provider: str = "placeholder"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    llm_model: str = "gpt-4o"

    research_digest_to: str = "author@example.com"
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""

    instagram_handle: str = "papiroebers"
    instagram_url: str = "https://www.instagram.com/papiroebers"

    semantic_scholar_api_key: str = ""
    pubmed_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return Settings()
