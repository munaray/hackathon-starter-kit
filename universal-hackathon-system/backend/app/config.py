from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
from typing import List


class Settings(BaseSettings):
    secret_key: str = "dev_secret_change_me"
    access_token_expire_minutes: int = 60

    database_url: str = "sqlite:///./dev.db"
    redis_url: str = "redis://localhost:6379/0"

    cors_origins: List[AnyHttpUrl] | List[str] = ["http://localhost:5173"]

    smtp_host: str | None = None
    smtp_port: int | None = None
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_from: str | None = None

    scheduler_cron: str | None = None

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors(cls, v):  # type: ignore
        if isinstance(v, str):
            return [o.strip() for o in v.split(",") if o.strip()]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()