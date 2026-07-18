"""Application configuration utilities."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    app_env: str
    groq_api_key: str
    groq_api_url: str
    model_name: str


_DEFAULT_API_URL = "https://api.groq.com/openai/v1/chat/completions"
_DEFAULT_MODEL = "llama3-70b-8192"


def get_settings() -> Settings:
    """Return application settings from environment variables."""

    return Settings(
        app_env=os.getenv("APP_ENV", "development"),
        groq_api_key=os.getenv("GROQ_API_KEY", ""),
        groq_api_url=os.getenv("GROQ_API_URL", _DEFAULT_API_URL),
        model_name=os.getenv("LOR_MODEL_NAME", _DEFAULT_MODEL),
    )
