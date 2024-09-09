from fastapi import HTTPException
import pytest

from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
import jwt

from zentra_api.core.config import AuthConfig
from zentra_api.auth.security import SecurityUtils


class TestSecurityUtils:
    @pytest.fixture
    def security_utils(self) -> SecurityUtils:
        return SecurityUtils(
            auth=AuthConfig(
                SECRET_ACCESS_KEY="secretaccess", SECRET_REFRESH_KEY="secretrefresh"
            )
        )

    @staticmethod
    def test_hash_password(security_utils: SecurityUtils):
        password = "testpassword"
        hashed_password = security_utils.hash_password(password)
        assert security_utils.auth.pwd_context.verify(password, hashed_password)

    @staticmethod
    def test_verify_password(security_utils: SecurityUtils):
        password = "testpassword"
        hashed_password = security_utils.hash_password(password)
        assert security_utils.verify_password(password, hashed_password)
        assert not security_utils.verify_password("wrongpassword", hashed_password)

    @staticmethod
    def test_expiration_with_delta(security_utils: SecurityUtils):
        expires_delta = timedelta(minutes=5)
        tolerance = timedelta(seconds=2)
        expected_expire_time = datetime.now(timezone.utc) + expires_delta
        expire_time = security_utils.expiration("access", expires_delta)

        assert (
            abs((expire_time - expected_expire_time).total_seconds())
            <= tolerance.total_seconds()
        ), f"Expected expire time to be close to {expected_expire_time}, but got {expire_time}"

    @staticmethod
    def test_expiration_access_default(security_utils: SecurityUtils):
        tolerance = timedelta(seconds=2)
        expected_expire_time = datetime.now(timezone.utc) + security_utils.expire_mins(
            "access"
        )
        expire_time = security_utils.expiration("access")

        assert (
            abs((expire_time - expected_expire_time).total_seconds())
            <= tolerance.total_seconds()
        ), f"Expected expire time to be close to {expected_expire_time}, but got {expire_time}"

    @staticmethod
    def test_expiration_refresh_default(security_utils: SecurityUtils):
        tolerance = timedelta(seconds=2)
        expected_expire_time = datetime.now(timezone.utc) + security_utils.expire_mins(
            "refresh"
        )
        expire_time = security_utils.expiration("refresh")

        assert (
            abs((expire_time - expected_expire_time).total_seconds())
            <= tolerance.total_seconds()
        ), f"Expected expire time to be close to {expected_expire_time}, but got {expire_time}"

    @staticmethod
    def test_encrypt(security_utils: SecurityUtils):
        class TestModel(BaseModel):
            password: str

        model = TestModel(password="testpassword")
        encrypted_model = security_utils.encrypt(model, "password")
        assert security_utils.auth.pwd_context.verify(
            "testpassword", encrypted_model.password
        )

    @staticmethod
    def test_encrypt_key_error(security_utils: SecurityUtils):
        class TestModel(BaseModel):
            password: str

        model = TestModel(password="testpassword")

        with pytest.raises(AttributeError):
            security_utils.encrypt(model, "email")

    @staticmethod
    def test_create_access_token(security_utils: SecurityUtils):
        data = {"sub": "testuser"}
        token = security_utils.create_access_token(data)
        decoded_data = jwt.decode(
            token,
            key=security_utils.auth.SECRET_ACCESS_KEY,
            algorithms=[security_utils.auth.ALGORITHM],
        )
        assert decoded_data["sub"] == "testuser", (token, decoded_data)

    @staticmethod
    def test_create_refresh_token(security_utils: SecurityUtils):
        data = {"sub": "testuser"}
        token = security_utils.create_refresh_token(data)
        decoded_data = jwt.decode(
            token,
            key=security_utils.auth.SECRET_REFRESH_KEY,
            algorithms=[security_utils.auth.ALGORITHM],
        )
        assert decoded_data["sub"] == "testuser", (token, decoded_data)

    @staticmethod
    def test_verify_access_token(security_utils: SecurityUtils):
        data = {"sub": "testuser"}
        token = security_utils.create_access_token(data)
        token_data = security_utils.verify_access_token(token)
        assert token_data == "testuser"

    @staticmethod
    def test_verify_refresh_token(security_utils: SecurityUtils):
        data = {"sub": "testuser"}
        token = security_utils.create_refresh_token(data)
        token_data = security_utils.verify_refresh_token(token)
        assert token_data == "testuser"

    @staticmethod
    def test_invalid_access_token(security_utils: SecurityUtils):
        with pytest.raises(HTTPException):
            security_utils.verify_access_token("invalidtoken")

    @staticmethod
    def test_invalid_refresh_token(security_utils: SecurityUtils):
        with pytest.raises(HTTPException):
            security_utils.verify_refresh_token("invalidtoken")

    @staticmethod
    def test_empty_token_data_access(security_utils: SecurityUtils):
        data = {"sub": None}
        token = security_utils.create_access_token(data)

        with pytest.raises(HTTPException):
            security_utils.verify_access_token(token)

    @staticmethod
    def test_empty_token_data_refresh(security_utils: SecurityUtils):
        data = {"sub": None}
        token = security_utils.create_access_token(data)

        with pytest.raises(HTTPException):
            security_utils.verify_refresh_token(token)
