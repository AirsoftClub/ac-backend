from fastapi import APIRouter, Depends

from app.dependencies import get_repository
from app.repositories import FieldRepository
from app.schemas import FieldDistanceResponse, FieldResponse

router = APIRouter()


@router.get(
    "/",
)
async def get_fields(
    field_repository: FieldRepository = Depends(get_repository(FieldRepository)),
) -> list[FieldResponse]:
    return await field_repository.get_all()


@router.get("/location", response_model=list[FieldDistanceResponse])
async def get_fields_by_location(
    latitude: float,
    longitude: float,
    field_repository: FieldRepository = Depends(get_repository(FieldRepository)),
):
    return [
        {
            "id": field.id,
            "name": field.name,
            "description": field.description,
            "tags": field.tags,
            "latitude": field.latitude,
            "longitude": field.longitude,
            "distance": distance,
        }
        for field, distance in await field_repository.get_all_by_distance(
            latitude, longitude
        )
    ]


@router.get("/{field_id}", response_model=FieldResponse)
async def get_field(
    field_id: int,
    field_repository: FieldRepository = Depends(get_repository(FieldRepository)),
):
    return await field_repository.get(field_id)


@router.get("/tag/{tag_id}", response_model=list[FieldResponse])
async def get_fields_by_tag_id(
    tag_id: int,
    field_repository: FieldRepository = Depends(get_repository(FieldRepository)),
):
    return await field_repository.get_by_tag(tag_id)
