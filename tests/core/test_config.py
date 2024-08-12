import pytest

from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from zentra_api.core.config import EmailConfig, DatabaseConfig, AuthConfig


@pytest.fixture
def email_config() -> EmailConfig:
    return EmailConfig(
        SMTP_TLS=True,
        SMTP_SSL=False,
        SMTP_PORT=587,
        SMTP_HOST="smtp.example.com",
        SMTP_USER="user@example.com",
        SMTP_PASSWORD="password",
        TEST_USER="test@example.com",
        FROM_EMAIL="noreply@example.com",
        FROM_NAME="Example",
        RESET_TOKEN_EXPIRE_HOURS=48,
    )


@pytest.fixture
def database_config() -> DatabaseConfig:
    return DatabaseConfig(
        URL="postgresql://user:password@localhost/dbname",
        FIRST_SUPERUSER="admin@example.com",
        FIRST_SUPERUSER_PASSWORD="supersecret",
    )


@pytest.fixture
def auth_config() -> AuthConfig:
    return AuthConfig(
        SECRET_KEY="supersecret",
        ALGORITHM="HS256",
        ACCESS_TOKEN_EXPIRE_MINUTES=10080,
        TOKEN_URL="auth/token",
        ROUNDS=12,
    )


class TestEmailConfig:
    @staticmethod
    def test_enabled_true(email_config: EmailConfig):
        assert email_config.enabled is True

    @staticmethod
    def test_enabled_false(email_config: EmailConfig):
        email_config.SMTP_HOST = None
        assert email_config.enabled is False


class TestDatabaseConfig:
    @staticmethod
    def test_validate_db_url_invalid():
        with pytest.raises(ValidationError):
            DatabaseConfig(
                URL="invalid_url",
                FIRST_SUPERUSER="admin@example.com",
                FIRST_SUPERUSER_PASSWORD="supersecret",
            )

    @staticmethod
    def test_init(database_config: DatabaseConfig):
        assert isinstance(database_config.URL, str)


class TestAuthConfig:
    @staticmethod
    def test_pwd_context_valid(auth_config: AuthConfig):
        assert hasattr(auth_config, "pwd_context")
        assert auth_config.pwd_context.rounds == auth_config.ROUNDS

    @staticmethod
    def test_oauth_scheme_valid(auth_config: AuthConfig):
        assert hasattr(auth_config, "oauth2_scheme")
        assert isinstance(auth_config.oauth2_scheme, OAuth2PasswordBearer)
