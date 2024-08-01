import pytest

from app.main import app
from app.config import get_db

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session


DB_URL = "sqlite:///:memory:"

test_engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture
def client() -> TestClient:
    app.dependency_overrides[get_db] = get_test_db
    return TestClient(app)


def get_test_db():
    """Dependency for retrieving a database session."""
    db: Session = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


def setup() -> None:
    from app.config import SETTINGS

    SETTINGS.SQL.Base.metadata.create_all(bind=test_engine)


def teardown() -> None:
    from app.config import SETTINGS

    SETTINGS.SQL.Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    """Fixture to run setup and teardown before and after the test session."""
    setup()
    yield
    teardown()
