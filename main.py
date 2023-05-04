from fastapi import FastAPI
from fastapi_health import health

from app.endpoints import health_checks, home_router


def create_app():
    app = FastAPI()
    # Add health check endpoint
    app.add_api_route("/health", health(health_checks), tags=["Health"])

    # Add routers
    app.include_router(home_router, tags=["Home"])

    return app


app = create_app()
