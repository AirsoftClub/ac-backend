from pydantic import BaseModel

from app.schemas.files import HasFiles


class Member(BaseModel):
    class Config:
        orm_mode = True

    id: int
    full_name: str


class CreateSquad(BaseModel):
    name: str
    emblem: str | None


class SquadResponse(HasFiles, BaseModel):
    class Config:
        orm_mode = True

    id: int
    name: str
    emblem: str


class SquadMembersResponse(SquadResponse):
    members: list[Member] = []


class AddMemberRequest(BaseModel):
    user_id: int
