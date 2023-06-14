from pydantic import BaseModel, Field

from app.schemas.files import HasFiles


class Member(BaseModel):
    class Config:
        orm_mode = True

    id: int
    full_name: str


class CreateSquad(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    emblem: str | None


class SquadResponse(HasFiles, BaseModel):
    class Config:
        orm_mode = True

    id: int
    name: str
    emblem: str | None


class SquadMembersResponse(SquadResponse):
    members: list[Member] = []


class AddMemberRequest(BaseModel):
    user_id: int
