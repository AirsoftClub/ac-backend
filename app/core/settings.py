from pydantic import BaseModel, BaseSettings


class Google(BaseModel):
    AUTHORIZATION_URL: str


class Database(BaseModel):
    URL: str


class Admin(BaseModel):
    USER: str
    PASSWORD: str


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        case_sensitive = True

    GOOGLE: Google
    DATABASE: Database
    ADMIN: Admin
    authjwt_secret_key: str = "secret"


settings = Settings()
