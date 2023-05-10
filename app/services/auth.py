from fastapi import status
from httpx import AsyncClient

from app.core.exceptions import Unauthenticated
from app.core.settings import settings
from app.schemas import AuthProvider, UserSchema


class AuthService:
    def __init__(self, http_client: AsyncClient):
        self.http_client = http_client

    async def authenticate(self, provider: AuthProvider, headers: dict):
        if provider == AuthProvider.Google:
            return await self.authenticate_google(headers)

    async def authenticate_google(self, headers: dict) -> UserSchema:
        response = await self.http_client.get(
            settings.GOOGLE.AUTHORIZATION_URL, headers=headers
        )
        if response.status_code != status.HTTP_200_OK:
            raise Unauthenticated

        user_info = response.json()
        return UserSchema(
            first_name=user_info["given_name"],
            last_name=user_info["family_name"],
            email=user_info["email"],
            image=user_info["picture"],
        )
