from pydantic import BaseModel, BaseSettings


class Google(BaseModel):
    AUTHORIZATION_URL: str = "https://www.googleapis.com/oauth2/v3/userinfo"


class Database(BaseModel):
    URL: str


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        case_sensitive = True

    GOOGLE: Google
    DATABASE: Database


settings = Settings()
