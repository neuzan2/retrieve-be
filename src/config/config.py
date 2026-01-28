from functools import cached_property, lru_cache
from pathlib import Path
from typing import Dict, List, Union

from pydantic_settings import BaseSettings

__all__ = ["settings"]


class Settings(BaseSettings):
    # Core settings
    APP_NAME: str = "FastAPI Backend"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_CONFIGS: List[Dict[str, Union[str, bool]]] = [
        {"version": "v1", "is_active": True},
        {"version": "v2", "is_active": True},
    ]

    # AWS settings
    AWS_REGION: str = "us-east-1"
    CLOUDWATCH_LOG_GROUP: str = ""
    CLOUDWATCH_LOG_STREAM: str = ""

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @cached_property
    def BASE_DIR(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @cached_property
    def SRC_DIR(self) -> Path:
        return self.BASE_DIR / "src"

    @cached_property
    def APP_DIR(self) -> Path:
        return self.BASE_DIR / "src/modules"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
