from pydantic import ValidationError
import pytest
from sqlalchemy import Engine
from pydantic_core import PydanticCustomError

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
        result = parse_cors(v=["http://127.0.0.1", "http://localhost:8080"])
        assert result == ["http://127.0.0.1", "http://localhost:8080"]

    @staticmethod
    def test_string():
        result = parse_cors(v="http://127.0.0.1,http://localhost:8080")
        assert result == ["http://127.0.0.1", "http://localhost:8080"]

    @staticmethod
    def test_invalid_input():
        with pytest.raises(ValidationError):
            parse_cors(12345)

    @staticmethod
    def test_invalid_string():
        with pytest.raises(PydanticCustomError):
            parse_cors("test123")

    @staticmethod
    def test_empty_string():
        assert parse_cors("") == []
