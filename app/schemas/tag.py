from pydantic import BaseModel


class TagResponse(BaseModel):
    class Config:
        orm_mode = True

    id: int
    description: str
