from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

Mode = Literal["fake", "real"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://app:app@localhost:5432/app"

    # Default mode for every capability (D-01):
    #   "fake": in-process fake adapters + mock-provider routes (v0)
    #   "real": real vendor adapters (v1; vendors are chosen in decisions.md)
    integrations_mode: Mode = "fake"

    # Per-capability override: add a `<capability>_mode: Mode | None = None` field, then read it
    # with mode_for("<capability>"). Env var: <CAPABILITY>_MODE.
    ai_mode: Mode | None = None

    # AI capability (D-05) — real mode only. Never commit the key: it lives in .env.
    anthropic_api_key: SecretStr | None = None
    ai_model: str = "claude-sonnet-5-5"
    ai_max_tokens: int = 1024

    def mode_for(self, capability: str) -> Mode:
        return getattr(self, f"{capability}_mode", None) or self.integrations_mode


settings = Settings()
