from app.auth.schema import UserBase

from zentra_api.responses import SuccessResponse
from zentra_api.schema import Token


class CreateUserResponse(SuccessResponse[UserBase]):
    """A response for creating the user."""

    pass


class LoginTokenResponse(SuccessResponse[Token]):
    """A response for getting the login token."""

    pass
