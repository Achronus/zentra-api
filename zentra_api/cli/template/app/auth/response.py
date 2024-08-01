from app.auth.schema import UserBase, GetUser

from zentra_api.responses import SuccessResponse


class CreateUserResponse(SuccessResponse[UserBase]):
    """A response for creating the user."""

    pass


class GetUserDetailsResponse(SuccessResponse[GetUser]):
    """A response for getting the user details."""

    pass
