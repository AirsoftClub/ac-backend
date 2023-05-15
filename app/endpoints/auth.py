from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from httpx import AsyncClient

from app.dependencies import get_http_client
from app.dependencies.repository import get_repository
from app.repositories import UserRepository
from app.schemas import RegisterRequest, RegisterResponse
from app.services import AuthService

router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
async def register(
    register_data: RegisterRequest,
    http_client: AsyncClient = Depends(get_http_client),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    Authorize: AuthJWT = Depends(),
):
    user_data = await AuthService(http_client).register(register_data)
    user = user_repo.create_or_update(user_data)

    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
def refresh(
    Authorize: AuthJWT = Depends(),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
):
    Authorize.jwt_refresh_token_required()

    email = Authorize.get_jwt_subject()

    # Check if the user exists in the database
    user_repo.get_by_email(email)

    new_access_token = Authorize.create_access_token(subject=email)
    return {"access_token": new_access_token}
