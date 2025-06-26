
import os
# Setting the Environment Variable Before Any App Imports
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["ADMIN_DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine, Session
from shifty.main import app
from shifty.infrastructure.db import get_session

# Use an in-memory SQLite database for testing
TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL)
TestSessionLocal = sessionmaker(class_=Session, autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Create tables before any tests run
    SQLModel.metadata.create_all(engine)
    yield
    # Drop tables after all tests are done
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(autouse=True)
def override_db_session():
    def override_get_session():
        session = TestSessionLocal()
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_session] = override_get_session
    yield
    app.dependency_overrides = {}

@pytest.fixture
def client(override_db_session, setup_database):
    return TestClient(app)
