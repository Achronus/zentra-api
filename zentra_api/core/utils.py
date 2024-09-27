"""
Utility functions for core logic in Zentra API projects.
"""

from sqlalchemy import Engine, create_engine, make_url, URL
from sqlalchemy.exc import ArgumentError

from pydantic import validate_call, ConfigDict
from pydantic_core import PydanticCustomError, Url, ValidationError


@validate_call(validate_return=True, config=ConfigDict(arbitrary_types_allowed=True))
def create_sql_engine(db_url: str) -> Engine:
    """
    Dynamically creates a simple SQL engine based on the given `db_url`.

    For more advanced and custom engines, use `sqlalchemy.create_engine()`.

    Parameters:
        db_url (str): The database URL.

    Returns:
        Engine: A SQLAlchemy engine.
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
    """
    Converts a number of days into minutes.

    Parameters:
        days (int): The number of days to convert.

    Returns:
        int: The number of minutes.
    """
    return 60 * 24 * days


@validate_call(validate_return=True)
def parse_cors(v: list | str) -> list[str]:
    """
    Validates a list, or comma separated string, of COR origin URLs.
    Returns them as a list of URLs.

    Parameters:
        v (list | str): A list or comma separated string of URLs.

    Returns:
        list[str]: A list of URLs.
    """
    if isinstance(v, str):
        if len(v) == 0:
            return []

        v = [i.strip() for i in v.split(",")]

    validated_urls = []
    for item in v:
        try:
            Url(url=item)
            validated_urls.append(item)
        except ValidationError:
            raise PydanticCustomError(
                "invalid_cors",
                f"'{item}' is not a valid COR origin URL.",
                dict(wrong_value=item),
            )

    return validated_urls
