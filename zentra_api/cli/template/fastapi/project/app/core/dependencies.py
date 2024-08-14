from typing import Annotated

from .db import get_db
from .config import SETTINGS

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

db_dependency = Annotated[Session, Depends(get_db)]
oauth2_dependency = Annotated[str, Depends(SETTINGS.AUTH.oauth2_scheme)]
oauth2_form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]
