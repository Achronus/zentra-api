"""
Security classes and methods for Zentra API projects.
"""

from datetime import datetime, timedelta, timezone
from typing import Literal

from zentra_api.core.config import AuthConfig
from zentra_api.responses import exceptions

import jwt
from pydantic import BaseModel


TokenTypeLiteral = Literal["access", "refresh"]


class SecurityUtils(BaseModel):
    """
    Contains utility methods for managing user authentication.

    ??? example "Example Usage"
        ```python
        from app.core.config import SETTINGS
        from zentra_api.auth.security import SecurityUtils

        security = SecurityUtils(auth=SETTINGS.AUTH)
        ```

    Parameters:
        auth (AuthConfig): a Zentra API AuthConfig model
    """

    auth: AuthConfig

    def hash_password(self, password: str) -> str:
        """
        Uses the [BcryptContext](/api/reference/auth/context/#zentra_api.auth.context.BcryptContext) to hash a password.

        ??? example "Example Usage"
            ```python
            from app.core.config import SETTINGS
            from zentra_api.auth.security import SecurityUtils

            security = SecurityUtils(auth=SETTINGS.AUTH)
            hashed_pass = security.hash_password("supersecretpassword")
            ```

        Parameters:
            password (str): a plain text password

        Returns:
            str: a hashed password
        """
        return self.auth.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Uses the [BcryptContext](/api/reference/auth/context/#zentra_api.auth.context.BcryptContext) to verify a password.

        ??? example "Example Usage"
            ```python
            from app.core.config import SETTINGS
            from zentra_api.auth.security import SecurityUtils

            security = SecurityUtils(auth=SETTINGS.AUTH)
            result = security.verify_password(
                plain_password="supersecretpassword",
                hashed_password="nelC0DeSokMRpjuCix70g-28BCMRqrrEgDRO5xBF0mY"
            )
            ```

        Parameters:
            plain_password (str): a plain text password
            hashed_password (str): a hashed password

        Returns:
            bool: True if the password is valid, False otherwise
        """
        return self.auth.pwd_context.verify(plain_password, hashed_password)

    def expiration(
        self, token_type: TokenTypeLiteral, expires_delta: timedelta | None = None
    ) -> datetime:
        """
        Creates an expiration datetime object for a JWT token.

        If `expires_delta=None`, automatically generates one using environment variables.

        ??? example "Example Usage"
            ```python
            from app.core.config import SETTINGS
            from zentra_api.auth.security import SecurityUtils

            security = SecurityUtils(auth=SETTINGS.AUTH)
            expiry = security.expiration('access')
            ```

        Parameters:
            token_type (TokenTypeLiteral): the type of token to create.

                Options: `access`, `refresh`

            expires_delta (timedelta): (optional) a timedelta object representing the expiration time. Can be manually provided. `None` by default.

                If `None`, it will use environment variables to calculate an appropriate duration based on token type.

                Defaults when `None`:

                - `access` token: 15 mins
                - `refresh` token: 7 days

                Environment variables to update token expiry length:

                - `access`: `AUTH__ACCESS_TOKEN_EXPIRE_MINS`
                - `refresh`: `AUTH__REFRESH_TOKEN_EXPIRE_MINS`

        Returns:
            datetime: a datetime object representing the expiration time
        """
        if expires_delta:
            return datetime.now(timezone.utc) + expires_delta

        return datetime.now(timezone.utc) + self.expire_mins(token_type)

    def expire_mins(self, token_type: TokenTypeLiteral) -> timedelta:
        """
        Returns the token expire minutes as a timedelta using environment variables.

        ??? example "Example Usage"
            ```python
            from app.core.config import SETTINGS
            from zentra_api.auth.security import SecurityUtils

            security = SecurityUtils(auth=SETTINGS.AUTH)
            expiry = security.expire_mins('access')
            ```

        Parameters:
            token_type (TokenTypeLiteral): the type of token to create.

                Options: `access`, `refresh`.

                Environment variables to update token expiry length:

                - `access`: `AUTH__ACCESS_TOKEN_EXPIRE_MINS`
                - `refresh`: `AUTH__REFRESH_TOKEN_EXPIRE_MINS`

                If not set, duration defaults:

                - `access` token: 15 mins
                - `refresh` token: 7 days




        Returns:
            timedelta: a timedelta object representing the expiration time
        """
        mins = (
            self.auth.ACCESS_TOKEN_EXPIRE_MINS
            if token_type == "access"
            else self.auth.REFRESH_TOKEN_EXPIRE_MINS
        )
        return timedelta(minutes=mins)

    def encrypt(self, model: BaseModel, attributes: str | list[str]) -> BaseModel:
        """
        Encrypts a set of data in a model and returns it as a new model.

        ??? example "Example Usage"
            ```python
            from app.core.config import SETTINGS
            from zentra_api.auth.security import SecurityUtils

            from pydantic import BaseModel, Field


            class UserBase(BaseModel):
                username: str = Field(..., description="A unique username to identify the user")


            class CreateUser(UserBase):
                password: str = Field(
                    ..., description="The users password to login to the platform"
                )
                is_active: bool = Field(default=True, description="The users account status")


            user = CreateUser(username="admin", password="supersecret")

            security = SecurityUtils(auth=SETTINGS.AUTH)

            # Example 1
            encrypted_user: CreateUser = security.encrypt(user, "password")

            # Example 2
            encrypted_user: CreateUser = security.encrypt(user, ["username", "password"])
            ```

        Parameters:
            model (BaseModel): a Pydantic BaseModel object
            attributes (str | list[str]): a string or list of strings representing the attributes to encrypt

        Returns:
            BaseModel: a new BaseModel object with the encrypted data
        """
        if isinstance(attributes, str):
            attributes = [attributes]

        data = model.model_dump()
        for attr in attributes:
            try:
                hashed_value = self.hash_password(getattr(model, attr))
                data[attr] = hashed_value

            except AttributeError:
                raise AttributeError(f"'{attr}' does not exist in '{type(model)}'!")

        return type(model)(**data)

    def _create_token(
        self,
        data: dict,
        secret_key: str,
        token_type: TokenTypeLiteral,
        expires_delta: timedelta | None = None,
    ) -> str:
        """
        A helper method for creating JWT tokens.

        Parameters:
            data (dict): a dictionary of data to encrypt
            secret_key (str): the secret key to use for encryption
            token_type (TokenTypeLiteral): the type of token to create.

                Options: `['access', 'refresh']`

            expires_delta (timedelta): (optional) a timedelta object representing the expiration time. Can be manually provided. `None` by default.

                If `None`, it will use environment variables to calculate an appropriate duration based on token type.

                Defaults when `None`:

                - `access` token: 15 mins
                - `refresh` token: 7 days

                Environment variables to update token expiry length:

                - `access`: `AUTH__ACCESS_TOKEN_EXPIRE_MINS`
                - `refresh`: `AUTH__REFRESH_TOKEN_EXPIRE_MINS`

        Returns:
            str: a JWT token
        """
        payload = data.copy()
        expire = self.expiration(token_type, expires_delta)

        payload.update({"exp": expire})
        encoded_jwt = jwt.encode(
            payload,
            key=secret_key,
            algorithm=self.auth.ALGORITHM,
        )
        return encoded_jwt

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        """
        Creates a JWT access token for the given data and returns it.

        ??? example "Example Usage"
            ```python
            from app.core.config import SETTINGS
            from zentra_api.auth.security import SecurityUtils

            security = SecurityUtils(auth=SETTINGS.AUTH)
            security.create_access_token({"sub": "admin"})
            ```

        Parameters:
            data (dict): a dictionary of data to encrypt
            expires_delta (timedelta): (optional) a timedelta object representing the expiration time. Can be manually provided. `None` by default.

                If `None`, it will use the environment variable `AUTH__ACCESS_TOKEN_EXPIRE_MINS` to calculate the access token duration.

                If `None` and no `AUTH__ACCESS_TOKEN_EXPIRE_MINS`, duration is set to `15 mins`.

        Returns:
            str: a JWT access token
        """
        return self._create_token(
            data,
            secret_key=self.auth.SECRET_ACCESS_KEY,
            token_type="access",
            expires_delta=expires_delta,
        )

    def create_refresh_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        """
        Creates a JWT refresh token for the given data and returns it.

        ??? example "Example Usage"
            ```python
            from app.core.config import SETTINGS
            from zentra_api.auth.security import SecurityUtils

            security = SecurityUtils(auth=SETTINGS.AUTH)
            security.create_refresh_token({"sub": "admin"})
            ```

        Parameters:
            data (dict): a dictionary of data to encrypt
            expires_delta (timedelta): (optional) a timedelta object representing the expiration time. Can be manually provided. `None` by default.

                If `None`, it will use the environment variable `AUTH__REFRESH_TOKEN_EXPIRE_MINS` to calculate the refresh token duration.

                If `None` and no `AUTH__REFRESH_TOKEN_EXPIRE_MINS`, duration is set to `7 days`.

        Returns:
            str: a JWT refresh token
        """
        return self._create_token(
            data,
            secret_key=self.auth.SECRET_REFRESH_KEY,
            token_type="refresh",
            expires_delta=expires_delta,
        )

    def _verify_token(self, token: str, secret_key: str) -> str:
        """
        A helper method for verifying the validity of a JWT token. Returns the token data if valid.

        Parameters:
            token (str): a JWT token
            secret_key (str): the secret key to use for decryption

        Returns:
            str: the token data
        """
        try:
            payload: dict = jwt.decode(
                token,
                key=secret_key,
                algorithms=[self.auth.ALGORITHM],
            )
            token_data: str | None = payload.get("sub")

            if token_data is None:
                raise exceptions.INVALID_CREDENTIALS

            return token_data

        except jwt.InvalidTokenError:
            raise exceptions.INVALID_CREDENTIALS

    def verify_access_token(self, token: str) -> str:
        """
        Verifies the validity of a JWT access token based on the `AUTH__SECRET_ACCESS_KEY` environment variable.

        Returns the token data if valid.

        ??? Example "Example Usage"
            ```python
            from app.core.config import SETTINGS
            from zentra_api.auth.security import SecurityUtils

            security = SecurityUtils(auth=SETTINGS.AUTH)
            security.verify_access_token(
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzI3NTI0MzMwfQ.cX0COXJkSYTtcbS9YIRhv0L9f4YhzWSxmD_mqZJ64IE"
            )
            ```

        Parameters:
            token (str): a JWT access token

        Returns:
            str: the token data
        """
        return self._verify_token(token, secret_key=self.auth.SECRET_ACCESS_KEY)

    def verify_refresh_token(self, token: str) -> str:
        """
        Verifies the validity of a JWT refresh token based on the `AUTH__SECRET_REFRESH_KEY` environment variable.

        Returns the token data if valid.

        ??? Example "Example Usage"
            ```python
            from app.core.config import SETTINGS
            from zentra_api.auth.security import SecurityUtils

            security = SecurityUtils(auth=SETTINGS.AUTH)
            security.verify_refresh_token(
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzI4MTI4MjMwfQ.PUB5aAuyMwyAN4erInj1vvZQT5sv50emQxJ8lrDMkVc"
            )
            ```

        Parameters:
            token (str): a JWT refresh token

        Returns:
            str: the token data
        """
        return self._verify_token(token, secret_key=self.auth.SECRET_REFRESH_KEY)
