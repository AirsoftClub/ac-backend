from pydantic import BaseModel

from app.schemas.tag import TagResponse


class FieldResponse(BaseModel):
    class Config:
        orm_mode = True

    id: int
    name: str
    description: str
    tags: list[TagResponse]
    latitude: float = None
    longitude: float = None


class FieldDistanceResponse(FieldResponse):
    class Config:
        orm_mode = False

    distance: float
