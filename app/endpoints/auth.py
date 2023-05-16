from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from httpx import AsyncClient

from app.dependencies import get_http_client
from app.dependencies.repository import get_repository
from app.repositories import UserRepository
from app.schemas import AccessTokenResponse, RegisterRequest
from app.schemas.auth import RefreshTokenResponse
from app.services import AuthService
from app.services.jwt import JWTService

router = APIRouter()


@router.post("/register", response_model=AccessTokenResponse)
async def register(
    register_data: RegisterRequest,
    http_client: AsyncClient = Depends(get_http_client),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    jwt_service: JWTService = Depends(),
):
    user_data = await AuthService(http_client).register(register_data)
    user = user_repo.create_or_update(user_data)

    return jwt_service.create_access_token(subject=user.email)


@router.post("/refresh", response_model=RefreshTokenResponse)
def refresh(
    Authorize: AuthJWT = Depends(),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    jwt_service: JWTService = Depends(),
):
    Authorize.jwt_refresh_token_required()

    email = Authorize.get_jwt_subject()

    # Check if the user exists in the database
    user_repo.get_by_email(email)

    return jwt_service.refresh_token(subject=email)
