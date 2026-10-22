from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://app:app@localhost:5432/app"
    # "fake": external systems are served by in-process fake adapters + mock-provider routes.
    # "real": real adapters (none exist yet — see docs/02-integrations.md).
    integrations_mode: Literal["fake", "real"] = "fake"


settings = Settings()
