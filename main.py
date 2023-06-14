from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_health import health
from fastapi_jwt_auth import AuthJWT

from app.core.exceptions import register_exception_handler
from app.core.settings import Settings
from app.dependencies import get_current_user
from app.endpoints import (
    auth_router,
    field_router,
    health_checks,
    home_router,
    register_admin,
    squad_router,
    user_router,
)
from app.models import Base, engine


def create_app():
    app = FastAPI()
    # Add health check endpoint
    app.add_api_route("/health", health(health_checks), tags=["Health"])

    # Add routers
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(home_router, tags=["Home"])
    app.include_router(user_router, prefix="/user", tags=["User"])
    app.include_router(
        field_router,
        prefix="/fields",
        tags=["Fields"],
        dependencies=[Depends(get_current_user)],
    )
    app.include_router(
        squad_router,
        prefix="/squads",
        tags=["Squads"],
        dependencies=[Depends(get_current_user)],
    )

    # Middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth_router, prefix="/auth", tags=["Auth"])

    # Auth config
    @AuthJWT.load_config
    def get_config():
        return Settings()

    # Exception handlers
    register_exception_handler(app)

    # Register admin
    register_admin(app)

    # Create tables
    Base.metadata.create_all(bind=engine)

    return app


app = create_app()
