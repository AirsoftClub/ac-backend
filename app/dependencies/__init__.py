from app.dependencies.db import get_db
from app.dependencies.http import get_http_client
from app.dependencies.repository import get_repository
from app.dependencies.user import get_current_admin, get_current_user

__all__ = [
    "get_client",
    "get_current_admin",
    "get_current_user",
    "get_db",
    "get_http_client",
    "get_repository",
]
