from zentra_api.auth.enums import JWTAlgorithm
from zentra_api.auth.context import BcryptContext

from sqlalchemy import URL, Engine, create_engine, make_url
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeMeta
from sqlalchemy.exc import ArgumentError

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, PrivateAttr, field_validator, ConfigDict
from pydantic_core import PydanticCustomError


class SQLConfig(BaseModel):
    """
    A model for storing SQL configuration settings. Automatically creates a SQL `engine`, `SessionLocal` and `Base` based on a given `db_url`.

    Parameters:
    - `db_url` - (`sqlalchemy.URL | string`) - the SQL database URL
    - `engine` (`sqlalchemy.Engine | None, optional`) - a custom SQLAlchemy engine instance created using `create_engine()`. When `None`, creates one automatically. `None` by default
    - `SessionLocal` (`sqlalchemy.sessionmaker | None, optional`) - a custom SQLAlchemy session instance created using `sessionmaker`. When `None`, creates one automatically -> `sessionmaker(autocommit=False, autoflush=False, bind=engine)`. `None` by default
    - `Base` (`sqlalchemy.orm.DeclarativeBase | None`) - a custom SQLAlchemy Base instance created using `declarative_base()`. When `None` creates one automatically -> `declarative_base()`. `None` by default
    """

    db_url: URL | str = Field(
        ...,
        description="The SQL database URL.",
    )
    engine: Engine | None = Field(
        None,
        description="A SQLAlchemy engine instance created using `create_engine()`.",
    )
    SessionLocal: sessionmaker | None = Field(
        None,
        description="a custom SQLAlchemy session instance created using `sessionmaker`.",
    )
    Base: DeclarativeMeta | None = Field(
        None,
        description="a custom SQLAlchemy Base instance created using `declarative_base()`.",
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("db_url")
    def validate_db_url(cls, db_url: URL | str) -> URL:
        if isinstance(db_url, str):
            try:
                db_url = make_url(db_url)
            except ArgumentError:
                raise PydanticCustomError(
                    "invalid_url",
                    f"'{db_url}' is not a valid database URL.",
                    dict(wrong_value=db_url),
                )

        return db_url

    def model_post_init(self, __context):
        self.engine = self._set_engine(self.engine)
        self.SessionLocal = self._set_session_local(self.SessionLocal)
        self.Base = self._set_base(self.Base)

    def _set_engine(self, engine: Engine | None) -> Engine:
        """A helper method for creating the SQL `engine`."""
        if engine:
            return engine

        if self.db_url.drivername.startswith("sqlite"):
            return create_engine(
                self.db_url,
                connect_args={"check_same_thread": False},
            )

        return create_engine(self.db_url)

    def _set_session_local(self, SessionLocal: sessionmaker | None) -> sessionmaker:
        """A helper method for setting the SQL session."""
        if SessionLocal:
            return SessionLocal

        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def _set_base(cls, Base: DeclarativeMeta | None) -> DeclarativeMeta:
        """A helper method for setting the SQl declarative base."""
        return Base if Base else declarative_base()

    def create_all(self) -> None:
        """Creates all the database tables in the `Base` instance."""
        self.Base.metadata.create_all(bind=self.engine)


class AuthConfig(BaseModel):
    """
    A storage container for authentication settings. Automatically creates tokens and secret keys using the given algorithm.

    Parameters:
    - `SECRET_KEY` (`string`) - the key for signing JSON Web Tokens (JWT)
    - `ALGORITHM` (`zentra_api.auth.enums.JWTAlgorithm, optional`) - the encryption algorithm for the OAUTH2 token and secret key. `HS512` by default
    - `ACCESS_TOKEN_EXPIRE_MINS` (`integer, optional`) - the expire length for access tokens in minutes. Must be a minimum of `15`. `30` by default
    - `ROUNDS` (`integer, optional`) - the the computational cost factor for bcrypt hashing. `12` by default
    - `TOKEN_URL` (`string, optional`) - the URL for the `oauth2_scheme` where `OAUTH2PasswordBearer(tokenUrl=<TOKEN_URL>)`. `auth/token` by default
    """

    SECRET_KEY: str = Field(
        ..., description="the key for signing JSON Web Tokens (JWT)"
    )
    ALGORITHM: JWTAlgorithm = Field(
        default=JWTAlgorithm.HS512,
        description="The encryption algorithm for the OAUTH2 token and secret key.",
        validate_default=True,
    )
    ACCESS_TOKEN_EXPIRE_MINS: int = Field(
        default=30,
        ge=15,
        description="The expire length for the access token in minutes.",
    )
    ROUNDS: int = Field(
        default=12, description="the the computational cost factor for bcrypt hashing."
    )
    TOKEN_URL: str = Field(
        default="auth/token",
        description="The `tokenUrl` for the `oauth2_scheme` (`OAUTH2PasswordBearer`).",
    )

    _pwd_context = PrivateAttr(default=None)
    _oauth2_scheme = PrivateAttr(default=None)

    model_config = ConfigDict(use_enum_values=True)

    def model_post_init(self, __context):
        self._pwd_context = BcryptContext(rounds=self.ROUNDS)
        self._oauth2_scheme = OAuth2PasswordBearer(tokenUrl=self.TOKEN_URL)

    @property
    def pwd_context(self) -> BcryptContext:
        """The authentication password context."""
        return self._pwd_context

    @property
    def oauth2_scheme(self) -> OAuth2PasswordBearer:
        """The OAUTH2 dependency flow. Uses authentication using a bearer token obtained with a password with from `TOKEN_URL`."""
        return self._oauth2_scheme


class Settings(BaseModel):
    """
    A model for storing all config settings.

    Parameters:
    - `SQL` (`zentra_api.config.SQLConfig`) - a ZentraAPI `SQLConfig` model containing a database URL
    - `AUTH` (`zentra_api.config.AuthConfig`) - a ZentraAPI `AuthConfig` model with authentication configuration settings
    """

    SQL: SQLConfig
    AUTH: AuthConfig

    model_config = ConfigDict(use_enum_values=True)
