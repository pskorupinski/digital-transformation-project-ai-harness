from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://app:app@localhost:5432/app"
    # "fake": capabilities are served by in-process fake adapters + mock-provider routes (v0).
    # "real": real vendor adapters (v1; vendors are chosen in decisions.md, see D-01).
    integrations_mode: Literal["fake", "real"] = "fake"


settings = Settings()
