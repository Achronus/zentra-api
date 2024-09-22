"""
Custom [Pydantic](https://docs.pydantic.dev/latest/) models used
throughout the Zentra API package.
"""

from typing import Literal
from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    """
    A model for storing token data.

    Parameters:
        access_token (string): a JWT access token
        refresh_token (string): a JWT refresh token
        token_type (['bearer', 'api_key', 'oauth_access', 'oauth_refresh']): the token type.
    """

    access_token: str
    refresh_token: str
    token_type: Literal["bearer", "api_key", "oauth_access", "oauth_refresh"]

    model_config = ConfigDict(use_enum_values=True)
