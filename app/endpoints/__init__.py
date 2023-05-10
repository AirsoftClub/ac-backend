from app.endpoints.admin import register_admin
from app.endpoints.healthcheck import health_checks
from app.endpoints.home import router as home_router
from app.endpoints.user import router as user_router

__all__ = ["home_router", "health_checks", "user_router", "register_admin"]
