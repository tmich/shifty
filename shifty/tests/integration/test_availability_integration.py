import pytest
from uuid import uuid4
from datetime import date, time, datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from shifty.domain.entities import Availability
from shifty.infrastructure.db import get_session
from shifty.main import app
from shifty.application.dto.availability_dto import AvailabilityCreate

# Use an in-memory SQLite database for testing
TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def setup_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def test_session(setup_db):
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(test_session):
    # Override the get_session dependency
    def override_get_session():
        try:
            yield test_session
        finally:
            pass
    
    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides = {}

@pytest.fixture
def test_create_and_delete_availability(client, test_session):
    """Test creating an availability and then deleting it"""
    user_id = uuid4()
    org_id = uuid4()
    
    # First create an availability
    tomorrow = date.today() + timedelta(days=1)
    availability_data = {
        "user_id": str(user_id),
        "organization_id": str(org_id),
        "date": tomorrow.isoformat(),
        "start_time": "09:00:00",
        "end_time": "17:00:00",
        "note": "Test availability"
    }
    
    # Create the availability
    response = client.post("/availabilities/", json=availability_data)
    assert response.status_code == 201
    result = response.json()
    assert result["result"] == "success"
    availability_id = result["availability"]["id"]
    
    # Verify it exists
    response = client.get(f"/availabilities/{availability_id}")
    assert response.status_code == 200
    
    # Delete the availability
    response = client.delete(f"/availabilities/{availability_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    response = client.get(f"/availabilities/{availability_id}")
    assert response.status_code == 404