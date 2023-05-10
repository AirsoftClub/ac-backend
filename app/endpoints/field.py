from fastapi import APIRouter, Depends

from app.dependencies import get_repository
from app.repositories import FieldRepository
from app.schemas import FieldResponse

router = APIRouter()


@router.get("/")
async def get_fields(
    field_repository: FieldRepository = Depends(get_repository(FieldRepository)),
) -> list[FieldResponse]:
    return field_repository.get_all()


@router.get("/tag/{tag_id}")
async def get_fields_by_tag(
    tag_id: int,
    field_repository: FieldRepository = Depends(get_repository(FieldRepository)),
) -> list[FieldResponse]:
    return field_repository.get_by_tag(tag_id)
