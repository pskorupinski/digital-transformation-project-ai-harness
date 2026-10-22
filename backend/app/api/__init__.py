from fastapi import APIRouter

from app.api import health

api_router = APIRouter()
api_router.include_router(health.router)
# Register feature routers here: api_router.include_router(<feature>.router)
