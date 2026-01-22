from functools import cached_property
from pathlib import Path
from typing import List, Dict, Union

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Core settings
    APP_NAME: str = "FastAPI Backend"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

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
        {
            "version": "v1",
            "is_active": True
        },
        {
            "version": "v2",
            "is_active": True
        }
    ]

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
        return Path(__file__).parent.parent.parent

    @cached_property
    def SRC_DIR(self) -> Path:
        return self.BASE_DIR / "src"

    @cached_property
    def APP_DIR(self) -> Path:
        return self.BASE_DIR / "src/app"


settings = Settings()
