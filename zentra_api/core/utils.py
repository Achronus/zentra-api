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

    For more advanced and custom engines, use [`sqlalchemy.create_engine()`](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine).

    ??? example "Example Usage"
        ```python
        from app.core.config import SETTINGS
        from zentra_api.core.utils import create_sql_engine

        engine = create_sql_engine(SETTINGS.DB.URL)
        ```

    Parameters:
        db_url (str): The database URL.

    Returns:
        Engine: A [SQLAlchemy.engine.Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) instance.
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

    ??? example "Example Usage"
        ```python
        from zentra_api.core.utils import days_to_mins

        days = days_to_mins(10800)  # 7
        ```

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

    ??? example "Example Usage"
        ```python
        from zentra_api.core.utils import parse_cors

        # Example 1
        cors = parse_cors("http://127.0.0.1,http://localhost:8080")

        # Example 2
        cors = parse_cors(["http://127.0.0.1", "http://localhost:8080"])

        # Both output => ["http://127.0.0.1", "http://localhost:8080"]
        ```

        This is extremely useful for dynamically passing a list of CORs origins from a `.env` file like so:
        ```bash title=""
        BACKEND_CORS_ORIGINS="http://127.0.0.1,http://localhost:8080"
        ```

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
