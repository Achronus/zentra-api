from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.core.db import Base


class DBUser(Base):
    """A model of the `User` table."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)


class DBUserDetails(Base):
    """A model of the `UserDetails` table."""

    __tablename__ = "user_details"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email = Column(String, unique=True, default=None)
    phone = Column(String, unique=True, default=None)
    full_name = Column(String, default=None)
