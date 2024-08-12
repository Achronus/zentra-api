from pydantic import ValidationError
import pytest
from sqlalchemy import Engine
from pydantic_core import PydanticCustomError, Url

from zentra_api.core.utils import create_sql_engine, days_to_mins, parse_cors


class TestCreateSQLEngine:
    @staticmethod
    def test_postgres_url():
        engine = create_sql_engine("postgresql://user:password@postgresserver/db")
        assert isinstance(engine, Engine)

    @staticmethod
    def test_sqlite_url():
        engine = create_sql_engine("sqlite:///test.db")
        assert isinstance(engine, Engine)

    @staticmethod
    def test_invalid_url():
        with pytest.raises(PydanticCustomError):
            create_sql_engine("invalid_url")


class TestDaysToMins:
    @pytest.mark.parametrize(
        "days, expected_mins",
        [
            (1, 1440),
            (7, 10080),
            (0, 0),
            (-1, -1440),
        ],
    )
    def test_valid(self, days: int, expected_mins: int):
        assert days_to_mins(days) == expected_mins


class TestParseCors:
    @staticmethod
    def test_list():
        urls = [Url("http://example.com"), Url("https://example2.com")]
        parsed_urls = parse_cors(urls)
        assert parsed_urls == urls

    @staticmethod
    def test_string():
        url_string = "http://example.com, https://example2.com"
        parsed_urls = parse_cors(url_string)
        target = [Url("http://example.com"), Url("https://example2.com")]
        assert parsed_urls == target

    @staticmethod
    def test_invalid_input():
        with pytest.raises(ValidationError):
            parse_cors(12345)

    @staticmethod
    def test_empty_string():
        with pytest.raises(ValidationError):
            parse_cors("")
