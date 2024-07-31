import bcrypt
from pydantic import BaseModel


class BcryptContext(BaseModel):
    """
    A custom context for `bcrypt` hashing.

    Parameters:
    - `rounds` (`integer, optional`) - the computational cost factor for hashing. `12` by default
    """

    rounds: int = 12

    def hash(self, password: str) -> str:
        """
        Hashes a password. Returns the hashed password.

        Parameters:
        - `password` (`string`) - the plain password to hash
        """
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    def verify(self, password: str, hashed_password: str) -> bool:
        """
        Verifies a password against a given hash. Returns `True` if the password matches, `False` otherwise.

        Parameters:
        - `password` (`string`) - the plain password to verify
        - `hashed_password` (`string`) - The hashed password to verify against
        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
