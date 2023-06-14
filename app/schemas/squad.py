from pydantic import BaseModel, validator


class Member(BaseModel):
    class Config:
        orm_mode = True

    id: int
    full_name: str


class CreateSquad(BaseModel):
    name: str

    @validator("name")
    def validate_non_empty_name(cls, value) -> str:
        if len(value) < 3:
            raise ValueError("Name too short.")
        return value


class SquadResponse(BaseModel):
    class Config:
        orm_mode = True

    id: int
    name: str
    emblem: str | None


class SquadMembersResponse(SquadResponse):
    members: list[Member] = []


class AddMemberRequest(BaseModel):
    user_id: int
