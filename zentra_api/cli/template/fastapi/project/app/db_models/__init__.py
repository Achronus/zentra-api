from .user import DBUser, DBUserDetails

from zentra_api.crud import CRUD, UserCRUD


class DBConnections:
    """A place to store all table CRUD operations."""

    def __init__(self) -> None:
        self.user = UserCRUD(model=DBUser)
        self.user_details = CRUD(model=DBUserDetails)


CONNECT = DBConnections()
