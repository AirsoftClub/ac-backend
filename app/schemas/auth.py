from enum import Enum

from pydantic import BaseModel


class AuthProvider(str, Enum):
    Google = "google"
    Facebook = "facebook"


class RegisterRequest(BaseModel):
    provider: AuthProvider
    token: str


class RegisterResponse(BaseModel):
    access_token: str
    refresh_token: str
