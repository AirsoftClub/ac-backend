from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.schemas import User

router = APIRouter()


@router.get("/me", response_model=User)
async def user_info(
    user: User = Depends(get_current_user),
):
    return user
