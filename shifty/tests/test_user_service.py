import datetime
import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from shifty.application.use_cases.user_service import UserService
from shifty.domain.entities import User

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def service(mock_repository):
    return UserService(mock_repository)

def make_user(role="worker"):
    return User(
        id=uuid4(),
        full_name="Test User",
        email="test@example.com",
        organization_id=uuid4(),
        role=role,
        is_active=True,
        created_at=datetime.datetime.now(),
        updated_at=None
    )

def test_get_by_id(service, mock_repository):
    user = make_user()
    mock_repository.get_by_id.return_value = user
    result = service.get_by_id(user.id)
    assert result == user
    mock_repository.get_by_id.assert_called_once_with(user.id)

def test_get_all(service, mock_repository):
    users = [make_user(), make_user()]
    mock_repository.get_all.return_value = users
    result = service.get_all()
    assert result == users
    mock_repository.get_all.assert_called_once()

def test_add(service, mock_repository):
    user = make_user()
    mock_repository.add.return_value = user
    result = service.add(user)
    assert result == user
    mock_repository.add.assert_called_once_with(user)

def test_delete(service, mock_repository):
    user_id = uuid4()
    service.delete(user_id)
    mock_repository.delete.assert_called_once_with(user_id)

def test_get_by_role(service, mock_repository):
    users = [make_user(role="worker"), make_user(role="admin")]
    mock_repository.get_by_role.return_value = users
    result = service.get_by_role("worker")
    assert result == users
    mock_repository.get_by_role.assert_called_once_with("worker")
