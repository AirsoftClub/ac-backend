from pydantic import AnyHttpUrl, BaseModel

from app.schemas.squad import SquadResponse


class UserSchema(BaseModel):
    class Config:
        orm_mode = True

    first_name: str
    last_name: str
    email: str
    image: AnyHttpUrl = None
    squads: list[SquadResponse] = []
