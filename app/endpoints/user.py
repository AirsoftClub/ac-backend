from fastapi import APIRouter, Depends

from app.dependencies import get_current_admin, get_current_user
from app.schemas import UserSchema

router = APIRouter()


@router.get("/me")
async def user_info(
    user: dict = Depends(get_current_user),
) -> UserSchema:
    return user


@router.get("/me/admin", response_model=UserSchema)
async def admin_info(
    user: dict = Depends(get_current_admin),
) -> UserSchema:
    return user
