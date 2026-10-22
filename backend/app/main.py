from fastapi import FastAPI

from app.api import api_router
from app.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title="Digital transformation project API")
    app.include_router(api_router, prefix="/api")
    if settings.integrations_mode == "fake":
        from app.integrations.mock_providers import router as mock_router

        app.include_router(mock_router, prefix="/api")
    return app


app = create_app()
