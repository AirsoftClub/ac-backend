from pydantic import AnyHttpUrl, BaseModel


class User(BaseModel):
    name: str
    email: str
    image: AnyHttpUrl
