from .config import SETTINGS

from zentra_api.core.utils import create_sql_engine
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeMeta


engine = create_sql_engine(SETTINGS.DB.URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: DeclarativeMeta = declarative_base()


def get_db():
    """Dependency for retrieving a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
