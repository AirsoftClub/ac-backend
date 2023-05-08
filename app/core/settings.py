from pydantic import BaseModel, BaseSettings


class Google(BaseModel):
    APP_KEY: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    SERVER_METADATA_URL = "https://accounts.google.com/.well-known/openid-configuration"


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
