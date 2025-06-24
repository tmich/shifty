import pytest
from uuid import uuid4
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock
from shifty.api.routers import availabilities
from shifty.domain.exceptions import NotExistsException

app = FastAPI()
app.include_router(availabilities.router)
client = TestClient(app)

@pytest.fixture
def mock_availability_service():
    return Mock()

@pytest.fixture
def mock_get_availability_service(mock_availability_service):
    return lambda: mock_availability_service

@pytest.fixture
def override_get_availability_service(app, mock_get_availability_service):
    app.dependency_overrides[availabilities.get_availability_service] = mock_get_availability_service
    yield
    app.dependency_overrides = {}

@pytest.fixture
def test_delete_availability_successful(override_get_availability_service, mock_availability_service):
    """Test that deleting an existing availability returns 204 No Content"""
    test_id = uuid4()
    
    response = client.delete(f"/availabilities/{test_id}")
    
    assert response.status_code == 204
    mock_availability_service.delete.assert_called_once_with(test_id)

@pytest.fixture
def test_delete_availability_not_found(override_get_availability_service, mock_availability_service):
    """Test that deleting a non-existent availability returns 404 Not Found"""
    test_id = uuid4()
    mock_availability_service.delete.side_effect = NotExistsException("Not found")
    
    response = client.delete(f"/availabilities/{test_id}")
    
    assert response.status_code == 404
    mock_availability_service.delete.assert_called_once_with(test_id)