from pydantic import BaseModel

from app.schemas.tag import TagResponse


class FieldResponse(BaseModel):
    class Config:
        orm_mode = True

    name: str
    description: str
    tags: list[TagResponse]
