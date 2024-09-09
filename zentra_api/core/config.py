from typing import Self

from pydantic_core import PydanticCustomError
from zentra_api.auth.context import BcryptContext
from zentra_api.auth.enums import JWTAlgorithm
from zentra_api.core.utils import days_to_mins

from pydantic import BaseModel, ConfigDict, EmailStr, PrivateAttr, model_validator
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import make_url
from sqlalchemy.exc import ArgumentError


class EmailConfig(BaseModel):
    """Storage container for email settings."""

    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None

    TEST_USER: EmailStr = "test@example.com"
    FROM_EMAIL: EmailStr | None = None
    FROM_NAME: str | None = None

    RESET_TOKEN_EXPIRE_HOURS: int = 48

    @property
    def enabled(self) -> bool:
        """Checks if emails are enabled."""
        return bool(self.SMTP_HOST and self.FROM_EMAIL)


class DatabaseConfig(BaseModel):
    """Storage container for database settings."""

    URL: str

    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    @model_validator(mode="after")
    def validate_db_url(self) -> Self:
        try:
            make_url(self.URL)
        except ArgumentError:
            raise PydanticCustomError(
                "invalid_url",
                f"'{self.URL}' is not a valid database URL.",
                dict(wrong_value=self.URL),
            )

        return self


class AuthConfig(BaseModel):
    """
    Storage container for authentication settings.

    Parameters:
        SECRET_ACCESS_KEY (string): the JWT access token encryption key
        SECRET_REFRESH_KEY (string): the JWT refresh token encryption key
        ALGORITHM: (zentra_api.auth.enums.JWTAlgorithm, optional): the JWT encryption algorithm. Options: `['HS256', 'HS384', 'HS512']`. `HS256` by default
        ACCESS_TOKEN_EXPIRE_MINS (integer, optional): the number of minutes an access token is valid for. `15` by default
        REFRESH_TOKEN_EXPIRE_MINS (integer, optional): the number of minutes a refresh token is valid for. `10080` by default (7 days)
        TOKEN_URL (string, optional): the token route URL. `auth/token` by default
        ROUNDS (integer, optional): the computational cost factor for bcrypt hashing. `12` by default
    """

    SECRET_ACCESS_KEY: str
    SECRET_REFRESH_KEY: str
    ALGORITHM: JWTAlgorithm = JWTAlgorithm.HS256
    ACCESS_TOKEN_EXPIRE_MINS: int = 15
    REFRESH_TOKEN_EXPIRE_MINS: int = days_to_mins(7)
    TOKEN_URL: str = "auth/token"
    ROUNDS: int = 12

    _pwd_context = PrivateAttr(default=None)
    _oauth2_scheme = PrivateAttr(default=None)

    model_config = ConfigDict(use_enum_values=True)

    def model_post_init(self, __context) -> None:
        self._pwd_context = BcryptContext(rounds=self.ROUNDS)
        self._oauth2_scheme = OAuth2PasswordBearer(tokenUrl=self.TOKEN_URL)

    @property
    def pwd_context(self) -> BcryptContext:
        return self._pwd_context

    @property
    def oauth2_scheme(self) -> OAuth2PasswordBearer:
        return self._oauth2_scheme
