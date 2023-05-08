from fastapi import Depends, Request
from pydantic import ValidationError

from app.core.exceptions import Unauthorized
from app.dependencies.repository import get_repository
from app.models import User
from app.repositories import UserRepository
from app.schemas import UserSchema


def get_user_data(request: Request) -> UserSchema:
    user = request.session.get("user") or {}
    try:
        return UserSchema(**user)
    except ValidationError:
        raise Unauthorized


def get_current_user(
    user_data: UserSchema = Depends(get_user_data),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> User:
    return user_repo.get_by_email(user_data.email)


def get_current_admin(
    user_data: UserSchema = Depends(get_user_data),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> User:
    user = user_repo.get_by_email(user_data.email)

    if not user.is_admin:
        raise Unauthorized

    return user
