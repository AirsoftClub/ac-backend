from fastapi import Depends

from app.core.exceptions import Unauthorized
from app.dependencies.auth import authenticate_user
from app.dependencies.repository import get_repository
from app.models import User
from app.repositories import UserRepository
from app.schemas import UserSchema


def get_current_user(
    user_data: UserSchema = Depends(authenticate_user),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> User:
    return user_repo.create_or_update(user_data)


def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_admin:
        raise Unauthorized

    return current_user
