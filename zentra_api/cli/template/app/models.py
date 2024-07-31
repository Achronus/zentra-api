"""Contains all SQL database models and CRUD connections."""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .config import SETTINGS
from zentra_api.crud import CRUD, UserCRUD


class DBUser(SETTINGS.SQL.Base):
    """A model of the `User` table."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)


class DBUserDetails(SETTINGS.SQL.Base):
    """A model of the `UserDetails` table."""

    __tablename__ = "user_details"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email = Column(String, unique=True, default=None)
    phone = Column(String, unique=True, default=None)
    full_name = Column(String, default=None)


SETTINGS.SQL.create_all()


class DBConnections:
    """A place to store all table CRUD operations."""

    def __init__(self) -> None:
        self.user = UserCRUD(model=DBUser)
        self.user_details = CRUD(model=DBUserDetails)


CONNECT = DBConnections()
