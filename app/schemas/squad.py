from pydantic import BaseModel


class Member(BaseModel):
    class Config:
        orm_mode = True

    full_name: str
    id: int


class SquadResponse(BaseModel):
    class Config:
        orm_mode = True

    name: str
    emblem: str


class SquadMembersResponse(SquadResponse):
    members: list[Member] = []


class AddMemberRequest(BaseModel):
    user_id: int
