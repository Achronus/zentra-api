from fastapi import HTTPException, status

__all__ = (
    "INVALID_CREDENTIALS",
    "INVALID_USER_DETAILS",
    "INVALID_REFRESH_TOKEN",
    "USER_ALREADY_REGISTERED",
)

INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)

INVALID_USER_DETAILS = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password.",
    headers={"WWW-Authenticate": "Bearer"},
)

INVALID_REFRESH_TOKEN = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="Invalid refresh token.",
    headers={"WWW-Authenticate": "Bearer"},
)

USER_ALREADY_REGISTERED = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    detail="User already registered.",
)
