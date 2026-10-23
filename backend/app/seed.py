"""Demo/reference data so a slice can be tried by hand right after it is built.

Run: docker compose exec backend python -m app.seed
Idempotent: safe to run repeatedly. Each slice that needs data adds a function below and
calls it from main(), labelled with its feature ID.
"""

from sqlalchemy.orm import Session

from app.db import SessionLocal


def main() -> None:
    with SessionLocal() as db:
        seed(db)
        db.commit()


def seed(db: Session) -> None:
    """Add per-feature seed functions here, e.g. seed_f_01_services(db)."""


if __name__ == "__main__":
    main()
