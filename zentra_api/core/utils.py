from sqlalchemy import Engine, create_engine, make_url, URL
from sqlalchemy.exc import ArgumentError

from pydantic import AnyUrl, validate_call, ConfigDict
from pydantic_core import PydanticCustomError


@validate_call(validate_return=True, config=ConfigDict(arbitrary_types_allowed=True))
def create_sql_engine(db_url: str) -> Engine:
    """
    Dynamically creates a simple SQL engine based on the given `db_url`.

    For more advanced and custom engines, use `sqlalchemy.create_engine()`.
    """
    try:
        db_url: URL = make_url(db_url)
    except ArgumentError:
        raise PydanticCustomError(
            "invalid_url",
            f"'{db_url}' is not a valid database URL.",
            dict(wrong_value=db_url),
        )

    if db_url.drivername.startswith("sqlite"):
        return create_engine(
            db_url,
            connect_args={"check_same_thread": False},
        )

    return create_engine(db_url)


@validate_call(validate_return=True)
def days_to_mins(days: int) -> int:
    """Converts a number of days into minutes."""
    return 60 * 24 * days


@validate_call(validate_return=True)
def parse_cors(v: list | str) -> list[AnyUrl]:
    """Validates a list, or comma separated string, of COR origin URLs. Returns them as a list of URLs."""
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list):
        return v
