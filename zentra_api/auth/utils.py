import secrets
import string

from zentra_api.auth.enums import JWTSize

from pydantic import ConfigDict, validate_call


@validate_call(config=ConfigDict(use_enum_values=True))
def generate_secret_key(size: JWTSize = 256) -> str:
    """Generates a random secret key using Base64 URL-safe characters.

    Parameters:
    - `size` (`integer | zentra_api.auth.enums.JWTSize, optional`) - the size of the secret key in bits. Valid options: `['256', '384', '512']`. `256` by default

    Returns:
        `string`: a randomly generated secret key.
    """
    key_length = size // 8  # Convert bits to bytes
    chars_to_use = string.ascii_letters + string.digits + "-_"

    return "".join(secrets.choice(chars_to_use) for _ in range(key_length))
