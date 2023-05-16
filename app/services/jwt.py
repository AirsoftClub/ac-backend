import datetime
from calendar import timegm

from fastapi_jwt_auth import AuthJWT

from app.schemas.auth import AccessTokenResponse, RefreshTokenResponse


class JWTService:
    def _calculate_expiration_timestamp(self, seconds: int) -> int:
        expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)
        return timegm(expiration.timetuple()) * 1000

    def refresh_token(
        self, subject: str, expires_seconds: int = 7200
    ) -> RefreshTokenResponse:
        authorize = AuthJWT()
        expires_at = self._calculate_expiration_timestamp(expires_seconds)
        access_token = authorize.create_access_token(
            subject, expires_time=expires_seconds
        )
        return {
            "access_token": access_token,
            "expires_at": expires_at,
        }

    def create_access_token(
        self,
        subject: str,
        refresh_token: str = "",
        expires_seconds: int = 7200,
    ) -> AccessTokenResponse:
        """Creates access token with expiration date and refresh token if not passed"""
        authorize = AuthJWT()
        expires_at = self._calculate_expiration_timestamp(expires_seconds)
        access_token = authorize.create_access_token(
            subject=subject, expires_time=expires_seconds
        )
        if refresh_token == "":
            refresh_token = authorize.create_refresh_token(subject=subject)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at,
        }
