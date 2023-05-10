from pydantic import AnyHttpUrl, BaseModel


class UserSchema(BaseModel):
    class Config:
        orm_mode = True

    first_name: str
    last_name: str
    email: str
    image: AnyHttpUrl
    is_admin: bool = False
