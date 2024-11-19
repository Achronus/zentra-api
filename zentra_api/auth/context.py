"""
Custom hashing contexts for Zentra API projects.
"""

import bcrypt
from pydantic import BaseModel, Field


class BcryptContext(BaseModel):
    """
    A custom context for bcrypt hashing.

    ??? example "Example Usage"
        ```python
        from zentra_api.auth.context import BcryptContext

        bcrypt_context = BcryptContext(rounds=14)
        ```

    Parameters:
        rounds (int): (optional) the computational cost factor for hashing.

            Higher rounds increase security but also slow down the hashing process, making brute-force attacks more difficult.

            Defaults to `12`.
    """

    rounds: int = Field(
        default=12, description="The computational cost factor for hashing."
    )

    def hash(self, password: str) -> str:
        """
        Hashes a password and returns the new hashed password.

        ??? example "Example Usage"
            ```python
            from zentra_api.auth.context import BcryptContext

            bcrypt_context = BcryptContext()
            hashed = bcrypt_context.hash('secretpassword')
            ```

        Parameters:
            password (str): the plain password to hash

        Returns:
            str: The bcrypt's hexadecimal representation of the salt and hashed version of the password.
        """
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    def verify(self, password: str, hashed_password: str) -> bool:
        """
        Verifies a password against a given hash.

        Returns True if the password matches, False otherwise.

        ??? example "Example Usage"
            ```python
            from zentra_api.auth.context import BcryptContext

            bcrypt_context = BcryptContext()
            verify = bcrypt_context.verify(
                password='secretpassword',
                hashed_password='$2b$12$vXZLwyt45QGS7C5V5ysA2eNtyArSa9RThVzi9erupyi23ThLi628i'
            )
            ```

        Parameters:
            password (str): the plain password to verify
            hashed_password (str): The hashed password to verify against

        Returns:
           bool : True if the given plain text matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
