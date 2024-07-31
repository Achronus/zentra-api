from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class CreateUser(UserBase):
    password: str
    is_active: bool = True


class UserDetails(BaseModel):
    email: str | None = None
    phone: str | None = None
    full_name: str | None = None
    is_active: bool


class GetUser(UserBase, UserDetails):
    pass


class UserInDB(GetUser):
    password: str
