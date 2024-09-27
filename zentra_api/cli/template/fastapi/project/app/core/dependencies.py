from typing import Annotated

from .db import get_db
from .config import SETTINGS

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

DB_DEPEND = Annotated[Session, Depends(get_db)]

OAUTH2_DEPEND = Annotated[str, Depends(SETTINGS.AUTH.oauth2_scheme)]
OAUTH2_FORM_DEPEND = Annotated[OAuth2PasswordRequestForm, Depends()]
