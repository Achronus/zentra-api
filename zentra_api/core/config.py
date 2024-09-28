"""
Configuration models for Zentra API projects. Settings are modified using a `.env` file.
"""

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
    """
    Storage container for email settings.

    Parameters:
        SMTP_TLS (bool): (optional) Whether to use TLS for SMTP.

            Defaults to `True`.
        SMTP_SSL (bool): (optional) Whether to use SSL for SMTP.

            Defaults to `False`.
        SMTP_PORT (int): (optional) The port for the SMTP server.

            Defaults to `587`.
        SMTP_HOST (str | None): (optional) The host for the SMTP server.

            Defaults to `None`.
        SMTP_USER (str | None): (optional) The user for the SMTP server.

            Defaults to `None`.
        SMTP_PASSWORD (str | None): (optional) The password for the SMTP server.

            Defaults to `None`.
        TEST_USER (EmailStr): (optional) The test user email.

            Defaults to `test@example.com`.
        FROM_EMAIL (EmailStr | None): (optional) The sender's email.

            Defaults to `None`.
        FROM_NAME (str | None): (optional) The sender's name.

            Defaults to `None`.
        RESET_TOKEN_EXPIRE_HOURS (int): (optional) The number of hours a reset token is valid for.

            Defaults to `48`.
    """

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
    """
    Storage container for database settings.

    Parameters:
        URL (str): The database URL.
        FIRST_SUPERUSER (EmailStr): The first superuser's email.
        FIRST_SUPERUSER_PASSWORD (str): The first superuser's password.
    """

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
        SECRET_ACCESS_KEY (str): the JWT access token encryption key
        SECRET_REFRESH_KEY (str): the JWT refresh token encryption key
        ALGORITHM (JWTAlgorithm): (optional) the JWT encryption algorithm.

            Options: `HS256`, `HS384`, `HS512`.

            Defaults to `HS256`.
        ACCESS_TOKEN_EXPIRE_MINS (int): (optional) the number of minutes an access token is valid for.

            Defaults to `15`.
        REFRESH_TOKEN_EXPIRE_MINS (int): (optional) the number of minutes a refresh token is valid for.

            Defaults to 7 days (`10080`).
        TOKEN_URL (str): (optional) the token route URL.

            Defaults to `auth/token`.
        ROUNDS (int): (optional) the computational cost factor for bcrypt hashing.

            Defaults to `12`.
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
        """A [BcryptContext](/api/reference/auth/context/#zentra_api.auth.context.BcryptContext) class for bcrypt hashing."""
        return self._pwd_context

    @property
    def oauth2_scheme(self) -> OAuth2PasswordBearer:
        """A FastAPI [OAuth2PasswordBearer](https://fastapi.tiangolo.com/reference/security/#fastapi.security.OAuth2AuthorizationCodeBearer.scheme_name) class for OAuth2 flow authentication.

        Uses a bearer token obtained with a password."""
        return self._oauth2_scheme
