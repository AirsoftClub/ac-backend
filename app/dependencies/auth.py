from typing import Annotated

from fastapi import Depends, Header
from fastapi.security import HTTPBearer
from httpx import AsyncClient

from app.dependencies.http import get_http_client
from app.schemas import AuthProvider, UserSchema
from app.services import AuthService

security = HTTPBearer()


async def headers(
    headers: HTTPBearer = Depends(security),
) -> dict:
    return {"Authorization": f"Bearer {headers.credentials}"}


async def authenticate_user(
    provider: Annotated[AuthProvider, Header()],
    http_client: AsyncClient = Depends(get_http_client),
    headers: dict = Depends(headers),
) -> UserSchema:
    return await AuthService(http_client).authenticate(provider, headers)
