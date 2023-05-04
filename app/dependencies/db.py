from typing import Generator

from app.models.base import SessionLocal


def get_db() -> Generator[SessionLocal, None, None]:
    """
    Get a database connection from the pool.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
