from typing import Literal
from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    """
    A model for storing token data.

    Parameters:
        access_token (string): a JWT access token
        refresh_token (string): a JWT refresh token
        token_type (Literal[string]): the token type. Valid options: `['bearer', 'api_key', 'oauth_access', 'oauth_refresh']`
    """

    access_token: str
    refresh_token: str
    token_type: Literal["bearer", "api_key", "oauth_access", "oauth_refresh"]

    model_config = ConfigDict(use_enum_values=True)
