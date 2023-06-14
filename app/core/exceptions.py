from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException


class ResourceNotFound(Exception):
    def __init__(self, resource: str):
        self.resource = resource.capitalize()


class Unauthenticated(Exception):
    pass


class Unauthorized(Exception):
    pass


class ResourceNotUnique(Exception):
    def __init__(self, resource: str):
        self.resource = resource.capitalize()


def error_content_generator(messages: list[str]) -> dict:
    return {"detail": [{"msg": message}] for message in messages}


def register_exception_handler(app: FastAPI):
    @app.exception_handler(ResourceNotFound)
    def handle_resource_not_found(request: Request, exc: ResourceNotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_content_generator([f"{exc.resource} not found"]),
        )

    @app.exception_handler(Unauthorized)
    def handle_unauthorized(request: Request, exc: Unauthorized):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=error_content_generator(["Not authorized"]),
        )

    @app.exception_handler(Unauthenticated)
    def handle_unauthenticated(request: Request, exc: Unauthenticated):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=error_content_generator(["Not authenticated"]),
        )

    @app.exception_handler(AuthJWTException)
    def authjwt_exception_handler(request: Request, exc: AuthJWTException):
        return JSONResponse(
            status_code=exc.status_code, content=error_content_generator([exc.message])
        )

    @app.exception_handler(ResourceNotUnique)
    def handle_resource_not_unique(request: Request, exc: ResourceNotUnique):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_content_generator([f"{exc.resource} already exists"]),
        )
