from pydantic import BaseModel


class Member(BaseModel):
    class Config:
        orm_mode = True

    id: int
    full_name: str


class CreateSquad(BaseModel):
    name: str
    emblem: str


class SquadResponse(BaseModel):
    class Config:
        orm_mode = True

    id: int
    name: str
    emblem: str


class SquadMembersResponse(SquadResponse):
    members: list[Member] = []


class AddMemberRequest(BaseModel):
    user_id: int
