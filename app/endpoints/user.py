from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.schemas import UserSchema

router = APIRouter()


@router.get("/me")
async def user_info(
    user: dict = Depends(get_current_user),
) -> UserSchema:
    return user
