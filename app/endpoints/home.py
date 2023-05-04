from fastapi import APIRouter, Depends

from app.dependencies.db import get_db
from app.models import SessionLocal

router = APIRouter()


@router.get("/")
def home(session: SessionLocal = Depends(get_db)):
    return {"message": "Hello World"}
