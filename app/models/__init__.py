# Add your models here to make alembic migrations work
from app.models.base import Base, SessionLocal, engine
from app.models.field import Field
from app.models.squad import Squad
from app.models.tag import Tag
from app.models.user import User

__all__ = [
    "Base",
    "Field",
    "SessionLocal",
    "Squad",
    "Tag",
    "User",
    "engine",
]
