"""ORM models — one module per aggregate, e.g. app/models/<entity>.py.

Every model module MUST be imported here so Alembic autogenerate sees it:

    from app.models.<entity> import <Entity>  # noqa: F401
"""

from app.db import Base

__all__ = ["Base"]
