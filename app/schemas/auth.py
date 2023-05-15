from enum import Enum

from pydantic import BaseModel


class AuthProvider(str, Enum):
    Google = "google"
    Facebook = "facebook"


class RegisterRequest(BaseModel):
    provider: AuthProvider
    token: str


class AccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: int


class RefreshTokenResponse(BaseModel):
    access_token: str
    expires_at: int
