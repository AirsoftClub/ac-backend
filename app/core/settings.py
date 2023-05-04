from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    DATABASE_URL: str = "sqlite:///:memory:"


settings = Settings()
