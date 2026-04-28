import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


def _to_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    api_base_url: str = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")
    ui_base_url: str = os.getenv("UI_BASE_URL", "https://www.saucedemo.com")
    ui_username: str = os.getenv("UI_USERNAME", "standard_user")
    ui_password: str = os.getenv("UI_PASSWORD", "secret_sauce")
    ui_headless: bool = _to_bool(os.getenv("UI_HEADLESS", "false"))
    ui_slowmo_ms: int = int(os.getenv("UI_SLOWMO_MS", "500"))
    timeout_ms: int = int(os.getenv("TIMEOUT_MS", "10000"))


settings = Settings()
