from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int = 5432
    db_name: str

    secret_key: str
    redis_url: str = "redis://redis:6379"
    fhub_api_key: str
    alembic_sync_db_url: str

    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15


    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

settings = Settings()