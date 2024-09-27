"""
Custom HTTP exceptions for API routes.

Example usage:
```python
    from fastapi import FastAPI
    from zentra_api.responses import exceptions

    app = FastAPI()

    @app.get("/protected")
    async def protected_route(user: User = Depends(get_current_user)):
        if not user:
            raise exceptions.INVALID_CREDENTIALS
        return {"message": "Access granted"}
```

Example response for `INVALID_CREDENTIALS`:
```json
    {
        "status": "error",
        "code": 401,
        "response": "401_UNAUTHORIZED",
        "message": "Could not validate credentials.",
        "headers": {"WWW-Authenticate": "Bearer"}
    }
```
"""

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
"""
A `fastapi.HTTPException` for invalid credentials.

```python
HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)
```
"""

INVALID_USER_DETAILS = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password.",
    headers={"WWW-Authenticate": "Bearer"},
)
"""
A `fastapi.HTTPException` for invalid user details.

```python
HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password.",
    headers={"WWW-Authenticate": "Bearer"},
)
```
"""

INVALID_REFRESH_TOKEN = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="Invalid refresh token.",
    headers={"WWW-Authenticate": "Bearer"},
)
"""
A `fastapi.HTTPException` for invalid refresh tokens.

```python
HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid refresh token.",
    headers={"WWW-Authenticate": "Bearer"},
)
```
"""

USER_ALREADY_REGISTERED = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    detail="User already registered.",
)
"""
A `fastapi.HTTPException` for user already registered.

```python
HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User already registered.",
)
```
"""
