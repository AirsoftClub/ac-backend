from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_health import health

from app.core.exceptions import ResourceNotFound, Unauthenticated, Unauthorized
from app.endpoints import health_checks, home_router, user_router


def create_app():
    app = FastAPI()
    # Add health check endpoint
    app.add_api_route("/health", health(health_checks), tags=["Health"])

    # Add routers
    app.include_router(home_router, tags=["Home"])
    app.include_router(user_router, prefix="/user", tags=["User"])

    # Middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    @app.exception_handler(ResourceNotFound)
    def handle_resource_not_found(request: Request, exc: ResourceNotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"{exc.resource} not found"},
        )

    @app.exception_handler(Unauthorized)
    def handle_unauthorized(request: Request, exc: Unauthorized):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Not authorized"},
        )

    @app.exception_handler(Unauthenticated)
    def handle_unauthenticated(request: Request, exc: Unauthenticated):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "Not authenticated"},
        )

    return app


app = create_app()
