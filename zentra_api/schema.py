from typing import Literal
from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    """
    A model for storing token data.

    ??? example "Example Usage"
        ```python
        from zentra_api.schema import Token

        token = Token(
            access_token="eyJk.eyJzdWIiOiJ0ZXN0In0.BEoSzbLPZtTWHAZ7WFngy3q0A",
            refresh_token="eyJ0eXAiOiJ.eyJzdWIiOiJ0ZXN0In0.k2PvXCrEC7bpjvOvfwIJF40",
            token_type="bearer",
        )
        ```

    Parameters:
        access_token (str): a JWT access token.
        refresh_token (str): a JWT refresh token.
        token_type (Literal[str]): the token type.

            Options: `bearer`, `api_key`, `oauth_access`, `oauth_refresh`.
    """

    access_token: str
    refresh_token: str
    token_type: Literal["bearer", "api_key", "oauth_access", "oauth_refresh"]

    model_config = ConfigDict(use_enum_values=True)
