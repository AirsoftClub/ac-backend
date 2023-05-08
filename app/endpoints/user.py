from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models import User
from app.schemas import UserSchema

router = APIRouter()


@router.get("/me", response_model=UserSchema)
async def user_info(
    user: User = Depends(get_current_user),
):
    return user
