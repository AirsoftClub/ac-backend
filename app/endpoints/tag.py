from fastapi import APIRouter, Depends

from app.dependencies import get_repository
from app.repositories import TagRepository
from app.schemas import TagResponse

router = APIRouter()


@router.get("/")
async def get_tags(
    tag_repository: TagRepository = Depends(get_repository(TagRepository)),
) -> list[TagResponse]:
    return tag_repository.get_all()


@router.get("/{tag_id}")
async def get_tag(
    tag_id: int,
    tag_repository: TagRepository = Depends(get_repository(TagRepository)),
) -> TagResponse:
    return tag_repository.get(tag_id)
