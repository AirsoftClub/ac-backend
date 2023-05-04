from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    DATABASE_URL: str = "sqlite:///./sql_app.db"


settings = Settings()
