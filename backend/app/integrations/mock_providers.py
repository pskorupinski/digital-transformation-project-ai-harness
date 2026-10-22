"""Routes that stand in for external systems' UIs and callbacks (fake mode only).

Mounted at /api/mock-providers only when settings.integrations_mode == "fake".
Add one sub-router per faked system; never import this module from services.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/mock-providers", tags=["mock-providers"])
