from typing import Annotated, Literal, Self

from zentra_api.auth.security import SecurityUtils
from zentra_api.core.config import AuthConfig, DatabaseConfig, EmailConfig
from zentra_api.core.utils import parse_cors

from pydantic import AnyUrl, BeforeValidator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """A storage container for all config settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        env_nested_delimiter="__",
    )

    API_VERSION: str = "/api/v1"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    DOMAIN: str = "localhost"

    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: Annotated[
        str | list[AnyUrl], BeforeValidator(parse_cors)
    ] = []

    AUTH: AuthConfig
    EMAIL: EmailConfig
    DB: DatabaseConfig

    @model_validator(mode="after")
    def _set_default_from_email(self) -> Self:
        if not self.EMAIL.FROM_NAME:
            self.EMAIL.FROM_NAME = self.PROJECT_NAME
        return self


SETTINGS = Settings()
security = SecurityUtils(auth=SETTINGS.AUTH)
