from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from app.core.exceptions import Unauthorized
from app.dependencies.repository import get_repository
from app.models import User
from app.repositories import UserRepository


def get_current_user(
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    Authorize: AuthJWT = Depends(),
) -> User:
    Authorize.jwt_required()

    user_email = Authorize.get_jwt_subject()
    user = user_repo.get_by_email(user_email)
    return user


def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_admin:
        raise Unauthorized

    return current_user
