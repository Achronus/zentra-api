import pytest
from pydantic import ValidationError

from zentra_api.schema import Token


class TestToken:
    @staticmethod
    def test_init():
        token = Token(
            access_token="valid_access_token",
            refresh_token="valid_refresh_token",
            token_type="bearer",
        )

        assert isinstance(token, Token)
        assert token.access_token == "valid_access_token"
        assert token.refresh_token == "valid_refresh_token"
        assert token.token_type == "bearer"

    @staticmethod
    def test_invalid_access_token():
        with pytest.raises(ValidationError):
            Token(access_token=None, token_type="bearer")

    @staticmethod
    def test_invalid_token_type():
        with pytest.raises(ValidationError):
            Token(
                access_token="valid_access_token",
                refresh_token="valid_refresh_token",
                token_type="invalid_token_type",
            )

    @staticmethod
    def test_invalid_refresh_token():
        with pytest.raises(ValidationError):
            Token(
                access_token="valid_access_token",
                refresh_token=None,
                token_type="bearer",
            )

    @staticmethod
    def test_model_dump_valid():
        token = Token(
            access_token="valid_access_token",
            refresh_token="valid_refresh_token",
            token_type="bearer",
        )
        token_dict = token.model_dump()

        assert token_dict == {
            "access_token": "valid_access_token",
            "refresh_token": "valid_refresh_token",
            "token_type": "bearer",
        }
