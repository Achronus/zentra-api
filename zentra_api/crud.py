"""
CRUD operations for database tables.

Example:
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
        model (Type): The database table to operate on. E.g., `db_models.Item`
    """

    model: Type

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _get(self, db: Session, id: int) -> Any:
        """
        Utility method for getting a single item.

        Parameters:
            db (Session): The database session.
            id (int): The ID of the item to get.

        Returns:
            Any | None: The item if it exists, otherwise None.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, data: dict) -> Any:
        """
        Adds an item to the table.

        Parameters:
            db (Session): The database session.
            data (dict): The data to add to the table.

        Returns:
            Any: The item that was added.
        """
        item = self.model(**data)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def get(self, db: Session, id: int) -> Any | None:
        """
        Retrieves a single item from the table.

        Parameters:
            db (Session): The database session.
            id (int): The ID of the item to get.

        Returns:
            Any | None: The item if it exists, otherwise None.
        """
        return self._get(db, id)

    def get_multiple(self, db: Session, skip: int = 0, limit: int = 100) -> list[Any]:
        """
        Retrieves multiple items from a table.

        Parameters:
            db (Session): The database session.
            skip (int, optional): The number of items to skip. Defaults to 0.
            limit (int, optional): The number of items to return. Defaults to 100.

        Returns:
            list[Any]: A list of items from the table.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def update(self, db: Session, id: int, data: BaseModel) -> Any | None:
        """
        Updates an item in the table.

        Parameters:
            db (Session): The database session.
            id (int): The ID of the item to update.
            data (BaseModel): The data to update the item with.

        Returns:
            Any | None: The updated item if it exists, otherwise None.
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

        Parameters:
            db (Session): The database session.
            id (int): The ID of the item to delete.

        Returns:
            Any | None: The item that was deleted if it exists, otherwise None.
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
            db (Session): The database session.
            attr (str): The attribute to filter by.
            value (str): The value to filter by.

        Returns:
            Any | None: The user if it exists, otherwise None.
        """
        return db.query(self.model).filter(getattr(self.model, attr) == value).first()

    def create(self, db: Session, data: dict) -> Any:
        """
        Adds a user to the table.

        Parameters:
            db (Session): The database session.
            data (dict): The data to add to the table.

        Returns:
            Any: The user that was added.
        """
        item = self.model(**data)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def get_by_username(self, db: Session, username: str) -> Any | None:
        """
        Retrieves a single user from the table by username.

        Parameters:
            db (Session): The database session.
            username (str): The username of the user to retrieve.

        Returns:
            Any | None: The user if it exists, otherwise None.
        """
        return self._get(db, "username", username)

    def get_by_id(self, db: Session, id: int) -> Any | None:
        """
        Retrieves a single user from the table by ID.

        Parameters:
            db (Session): The database session.
            id (int): The ID of the user to retrieve.

        Returns:
            Any | None: The user if it exists, otherwise None.
        """
        return self._get(db, "id", id)

    def update(self, db: Session, id: int, data: BaseModel) -> Any | None:
        """
        Updates a users details in the table.

        Parameters:
            db (Session): The database session.
            id (int): The ID of the user to update.
            data (BaseModel): The data to update the user with.

        Returns:
            Any | None: The updated user if it exists, otherwise None.
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

        Parameters:
            db (Session): The database session.
            id (int): The ID of the user to delete.

        Returns:
            Any | None: The user that was deleted if it exists, otherwise None.
        """
        result = self._get(db, "id", id)

        if result:
            db.delete(result)
            db.commit()

        return result
