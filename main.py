import os
from fastapi import FastAPI
from fastapi_health import health

from app.endpoints import health_checks, home_router, login_router

from starlette.middleware.sessions import SessionMiddleware

from dotenv import load_dotenv


def create_app():
    app = FastAPI()
    # Add health check endpoint
    app.add_api_route("/health", health(health_checks), tags=["Health"])

    # Add routers
    app.include_router(home_router, tags=["Home"])
    app.include_router(login_router, tags=["Login"])

    # Middlewares
    app.add_middleware(SessionMiddleware, secret_key=os.environ.get("APP_KEY"))

    return app


load_dotenv()
app = create_app()
