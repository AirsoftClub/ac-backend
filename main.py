from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi_health import health
from starlette.middleware.sessions import SessionMiddleware

from app.core.exceptions import ResourceNotFound, Unauthorized
from app.core.settings import settings
from app.endpoints import auth_router, health_checks, home_router, user_router


def create_app():
    app = FastAPI()
    # Add health check endpoint
    app.add_api_route("/health", health(health_checks), tags=["Health"])

    # Add routers
    app.include_router(home_router, tags=["Home"])
    app.include_router(auth_router, tags=["Auth"])
    app.include_router(user_router, prefix="/user", tags=["User"])

    # Middlewares
    app.add_middleware(SessionMiddleware, secret_key=settings.GOOGLE.APP_KEY)

    # Exception handlers
    @app.exception_handler(ResourceNotFound)
    def handle_resource_not_found(request: Request, exc: ResourceNotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"{exc.resource} not found"},
        )

    @app.exception_handler(Unauthorized)
    def handle_unauthorized(request: Request, exc: Unauthorized):
        return RedirectResponse(request.url_for("login"))

    return app


app = create_app()
