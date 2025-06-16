import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import date, time, datetime

from shifty.application.use_cases.shift_service import ShiftService
from shifty.application.dto.shift_dto import ShiftCreate
from shifty.domain.entities import Shift

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def service(mock_repository):
    return ShiftService(mock_repository)

def make_shift():
    return Shift(
        id=uuid4(),
        user_id=uuid4(),
        organization_id=uuid4(),
        date=date.today(),
        start_time=time(9, 0),
        end_time=time(17, 0),
        note="test",
        created_at=datetime.now()
    )

def make_create_dto():
    return ShiftCreate(
        user_id=uuid4(),
        organization_id=uuid4(),
        date=date.today(),
        start_time=time(9, 0),
        end_time=time(17, 0),
        note="test"
    )

def test_create_success(service, mock_repository):
    dto = make_create_dto()
    expected = make_shift()
    mock_repository.add.return_value = expected
    result = service.create(dto)
    assert result == expected
    mock_repository.add.assert_called_once()

def test_list_all(service, mock_repository):
    expected = [make_shift()]
    mock_repository.get_all.return_value = expected
    result = service.list_all()
    assert result == expected
    mock_repository.get_all.assert_called_once()

def test_get_by_id_success(service, mock_repository):
    expected = make_shift()
    mock_repository.get_by_id.return_value = expected
    result = service.get_by_id(expected.id)
    assert result == expected
    mock_repository.get_by_id.assert_called_once_with(expected.id)

def test_get_by_id_not_found(service, mock_repository):
    mock_repository.get_by_id.return_value = None
    with pytest.raises(ValueError):
        service.get_by_id(uuid4())

def test_delete_success(service, mock_repository):
    service.delete(uuid4())
    mock_repository.delete.assert_called_once()

def test_delete_not_found(service, mock_repository):
    mock_repository.delete.side_effect = ValueError
    with pytest.raises(ValueError):
        service.delete(uuid4())