"""
CRUD operations for database tables.

??? example "Example Usage"
    ```python
    from zentra_api.crud import CRUD, UserCRUD

    from db_models import DBUser, DBUserDetails

    user = UserCRUD(model=DBUser)
    user_details = CRUD(model=DBUserDetails)
    ```
"""

from typing import Any, Type
from sqlalchemy.orm import Session

from pydantic import BaseModel, ConfigDict


class CRUD(BaseModel):
    """
    Handles create, read, update, and delete operations for a database table.

    Parameters:
        model (Type): The database table to operate on.
    """

    model: Type

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _get(self, db: Session, id: int) -> Any:
        """
        Utility method for getting a single item.

        Parameters:
            db (Session): The [`sqlalchemy.orm.Session`](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) database session.
            id (int): The ID of the item to get.

        Returns:
            item (Any | None): The item if it exists, otherwise `None`.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, data: dict) -> Any:
        """
        Adds an item to the table.

        ??? example "Example Usage"
            ```python
            from zentra_api.crud import CRUD
            from db_models import DBUserDetails
            from app.core.db import get_db


            class UserDetails(BaseModel):
                email: str | None = Field(default=None, description="The users email address")
                phone: str | None = Field(default=None, description="The users contact number")
                full_name: str | None = Field(default=None, description="The users full name")
                is_active: bool = Field(..., description="The users account status")


            db = Annotated[Session, Depends(get_db)]
            user_details = UserDetails(
                email="test@email.com",
                phone="+4412345679",
                full_name="John Doe"
                is_active=True,
            )

            details = CRUD(model=DBUserDetails)
            item: DBUserDetails = details.create(db, user_details.model_dump())
            ```

        Parameters:
            db (Session): The [`sqlalchemy.orm.Session`](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) database session.
            data (dict): The data to add to the table.

        Returns:
            item (Any):  A database table model of the item that was added.
        """
        item = self.model(**data)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def get(self, db: Session, id: int) -> Any | None:
        """
        Retrieves a single item from the table.


        ??? example "Example Usage"
            ```python
            from zentra_api.crud import CRUD
            from db_models import DBUserDetails
            from app.core.db import get_db


            db = Annotated[Session, Depends(get_db)]

            details = CRUD(model=DBUserDetails)
            item: DBUserDetails = details.get(db, 2)
            ```

        Parameters:
            db (Session): The [`sqlalchemy.orm.Session`](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) database session.
            id (int): The ID of the item to get.

        Returns:
            item (Any | None): A database table model of the item if it exists, otherwise `None`.
        """
        return self._get(db, id)

    def get_multiple(self, db: Session, skip: int = 0, limit: int = 100) -> list[Any]:
        """
        Retrieves multiple items from a table.


        ??? example "Example Usage"
            ```python
            from zentra_api.crud import CRUD
            from db_models import DBUserDetails
            from app.core.db import get_db


            db = Annotated[Session, Depends(get_db)]

            details = CRUD(model=DBUserDetails)
            items: list[DBUserDetails] = details.get_multiple(db, skip=0, limit=10)
            ```

        Parameters:
            db (Session): The [`sqlalchemy.orm.Session`](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) database session.
            skip (int): (optional) The number of items to skip.
            limit (int): (optional) The number of items to return.

        Returns:
            items (list[Any]): A list of database table models of the items from the table.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def update(self, db: Session, id: int, data: BaseModel) -> Any | None:
        """
        Updates an item in the table.

        ??? example "Example Usage"
            ```python
            from zentra_api.crud import CRUD
            from db_models import DBUserDetails
            from app.core.db import get_db


            class UserDetails(BaseModel):
                email: str | None = Field(default=None, description="The users email address")
                phone: str | None = Field(default=None, description="The users contact number")
                full_name: str | None = Field(default=None, description="The users full name")
                is_active: bool = Field(..., description="The users account status")


            db = Annotated[Session, Depends(get_db)]
            user_details = UserDetails(full_name="Jane Doe")

            details = CRUD(model=DBUserDetails)
            item: DBUserDetails | None = details.update(db, id=5, data=user_details)
            ```

        Parameters:
            db (Session): The [`sqlalchemy.orm.Session`](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) database session.
            id (int): The ID of the item to update.
            data (BaseModel): The data to update the item with.

        Returns:
            item (Any | None): The database table model of the item if it exists, otherwise `None`.
        """
        result = self._get(db, id)

        if not result:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(result, field, value)

        db.commit()
        db.refresh(result)
        return result

    def delete(self, db: Session, id: int) -> Any | None:
        """
        Deletes an item from the table.

        ??? example "Example Usage"
            ```python
            from zentra_api.crud import CRUD
            from db_models import DBUserDetails
            from app.core.db import get_db

            db = Annotated[Session, Depends(get_db)]

            details = CRUD(model=DBUserDetails)
            item: DBUserDetails = details.delete(db, id=3)
            ```

        Parameters:
            db (Session): The [`sqlalchemy.orm.Session`](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) database session.
            id (int): The ID of the item to delete.

        Returns:
            item (Any | None): The database table model of the item that was deleted if it exists, otherwise `None`.
        """
        result = self._get(db, id)

        if result:
            db.delete(result)
            db.commit()

        return result


class UserCRUD(BaseModel):
    """
    Handles create, read, update, and delete operations for the `User` database table.

    Parameters:
        model (Type): The `User` database table to operate on.
    """

    model: Type

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _get(self, db: Session, attr: str, value: str) -> Any:
        """
        Utility method for getting a single user.

        Parameters:
            db (Session): The [`sqlalchemy.orm.Session`](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) database session.
            attr (str): The attribute to filter by.
            value (str): The value to filter by.

        Returns:
           user (Any | None): The database table model of the user if it exists, otherwise `None`.
        """
        return db.query(self.model).filter(getattr(self.model, attr) == value).first()

    def create(self, db: Session, data: dict) -> Any:
        """
        Adds a user to the table.

        ??? example "Example Usage"
            ```python
            from zentra_api.crud import UserCRUD
            from db_models import DBUser
            from app.core.db import get_db


            class UserBase(BaseModel):
                username: str = Field(..., description="A unique username to identify the user")


            class CreateUser(UserBase):
                password: str = Field(
                    ..., description="The users password to login to the platform"
                )
                is_active: bool = Field(default=True, description="The users account status")


            db = Annotated[Session, Depends(get_db)]
            new_user = CreateUser(
                username="johndoe",
                password="supersecret",
            )

            user = UserCRUD(model=DBUser)
            user: DBUser = user.create(db, new_user.model_dump())
            ```

        Parameters:
            db (Session): The [`sqlalchemy.orm.Session`](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) database session.
            data (dict): The data to add to the table.

        Returns:
            user (Any): The database table model of the created user.
        """
        item = self.model(**data)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def get_by_username(self, db: Session, username: str) -> Any | None:
        """
        Retrieves a single user from the table by username.

        ??? example "Example Usage"
            ```python
            from zentra_api.crud import UserCRUD
            from db_models import DBUser
            from app.core.db import get_db


            db = Annotated[Session, Depends(get_db)]

            user = UserCRUD(model=DBUser)
            user: DBUser = user.get_by_username(db, "johndoe")
            ```

        Parameters:
            db (Session): The [`sqlalchemy.orm.Session`](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) database session.
            username (str): The username of the user to retrieve.

        Returns:
            user (Any | None): The database table model of the user if it exists, otherwise `None`.
        """
        return self._get(db, "username", username)

    def get_by_id(self, db: Session, id: int) -> Any | None:
        """
        Retrieves a single user from the table by ID.

        ??? example "Example Usage"
            ```python
            from zentra_api.crud import UserCRUD
            from db_models import DBUser
            from app.core.db import get_db


            db = Annotated[Session, Depends(get_db)]

            user = UserCRUD(model=DBUser)
            user: DBUser = user.get_by_id(db, id=3)
            ```

        Parameters:
            db (Session): The [`sqlalchemy.orm.Session`](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) database session.
            id (int): The ID of the user to retrieve.

        Returns:
            user (Any | None): The database table model of the user if it exists, otherwise `None`.
        """
        return self._get(db, "id", id)

    def update(self, db: Session, id: int, data: BaseModel) -> Any | None:
        """
        Updates a users details in the table.

        ??? example "Example Usage"
            ```python
            from zentra_api.crud import UserCRUD
            from db_models import DBUser
            from app.core.db import get_db


            class UpdateUser(BaseModel):
                username: str = Field(None, description="The new username for the user.")
                password: str = Field(None, description="The new login password for the user.")


            db = Annotated[Session, Depends(get_db)]
            new_details = UpdateUser(
                password="stillsecret",
            )

            user = UserCRUD(model=DBUser)
            user: DBUser = user.update(db, id=4, data=new_details.model_dump())
            ```

        Parameters:
            db (Session): The [`sqlalchemy.orm.Session`](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) database session.
            id (int): The ID of the user to update.
            data (BaseModel): The data to update the user with.

        Returns:
            user (Any | None): The database table model of the updated user if it exists, otherwise `None`.
        """
        result = self._get(db, "id", id)

        if not result:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(result, field, value)

        db.commit()
        db.refresh(result)
        return result

    def delete(self, db: Session, id: int) -> Any | None:
        """
        Deletes a user from the table.

        ??? example "Example Usage"
            ```python
            from zentra_api.crud import UserCRUD
            from db_models import DBUser
            from app.core.db import get_db


            db = Annotated[Session, Depends(get_db)]

            user = UserCRUD(model=DBUser)
            user: DBUser = user.delete(db, id=2)
            ```

        Parameters:
            db (Session): The [`sqlalchemy.orm.Session`](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) database session.
            id (int): The ID of the user to delete.

        Returns:
            user (Any | None): The database table model of the user that was deleted if it exists, otherwise `None`.
        """
        result = self._get(db, "id", id)

        if result:
            db.delete(result)
            db.commit()

        return result
