from app.endpoints.admin import register_admin
from app.endpoints.auth import router as auth_router
from app.endpoints.field import router as field_router
from app.endpoints.healthcheck import health_checks
from app.endpoints.home import router as home_router
from app.endpoints.squad import router as squad_router
from app.endpoints.user import router as user_router

__all__ = [
    "auth_router",
    "field_router",
    "health_checks",
    "home_router",
    "register_admin",
    "squad_router",
    "user_router",
]
