from enum import StrEnum


class JWTAlgorithm(StrEnum):
    """The type of JWT hashing algorithm to use."""

    HS256 = "HS256"
    """HMAC with SHA-256 algorithm."""
    HS384 = "HS384"
    """HMAC with SHA-384 algorithm."""
    HS512 = "HS512"
    """HMAC with SHA-512 algorithm."""
