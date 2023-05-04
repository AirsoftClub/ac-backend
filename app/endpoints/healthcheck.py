from fastapi import Depends

from app.dependencies import get_db
from app.models import SessionLocal


def is_database_online(session: SessionLocal = Depends(get_db)):
    if session:
        return {"database": "online"}
    return False


health_checks = [is_database_online]
