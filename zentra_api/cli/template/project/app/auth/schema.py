from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., description="A unique username to identify the user")


class CreateUser(UserBase):
    password: str = Field(
        ..., description="The users password to login to the platform"
    )
    is_active: bool = Field(default=True, description="The users account status")


class UserDetails(BaseModel):
    email: str | None = Field(default=None, description="The users email address")
    phone: str | None = Field(default=None, description="The users contact number")
    full_name: str | None = Field(default=None, description="The users full name")
    is_active: bool = Field(..., description="The users account status")


class GetUser(UserBase, UserDetails):
    pass
