from app.endpoints.admin import register_admin
from app.endpoints.field import router as field_router
from app.endpoints.healthcheck import health_checks
from app.endpoints.home import router as home_router
from app.endpoints.tag import router as tag_router
from app.endpoints.user import router as user_router

__all__ = [
    "field_router",
    "health_checks",
    "home_router",
    "register_admin",
    "tag_router",
    "user_router",
]
