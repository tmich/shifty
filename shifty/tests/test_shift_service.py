import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import date, time, datetime

from shifty.application.use_cases.shift_service import ShiftService
from shifty.application.dto.shift_dto import ShiftCreate
from shifty.domain.entities import Shift, ShiftType

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def service(mock_repository):
    return ShiftService(mock_repository)

def make_shift():
    user_id=uuid4()

    return Shift(
        id=uuid4(),
        user_id=user_id,
        origin_user_id=user_id,
        organization_id=uuid4(),
        date=date.today(),
        start_time=time(9, 0),
        end_time=time(17, 0),
        note="test",
        created_at=datetime.now()
    )

def make_create_dto():
    user_id = uuid4()

    return ShiftCreate(
        user_id=user_id,
        origin_user_id=user_id,
        organization_id=uuid4(),
        date=date.today(),
        start_time=time(9, 0),
        end_time=time(17, 0),
        note="test"
    )

def make_shift_type():
    return ShiftType(
        id=uuid4(),
        organization_id=uuid4(),
        name="Morning",
        start_time=time(8, 0),
        end_time=time(16, 0),
        description="Morning shift",
        is_active=True,
        created_at=datetime.now(),
        updated_at=None
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

def test_get_by_date(service, mock_repository):
    test_date = date.today()
    expected = [make_shift()]
    mock_repository.get_by_date.return_value = expected
    result = service.get_by_date(test_date)
    assert result == expected
    mock_repository.get_by_date.assert_called_once_with(test_date)

def test_get_by_user(service, mock_repository):
    user_id = uuid4()
    expected = [make_shift()]
    mock_repository.get_by_user.return_value = expected
    result = service.get_by_user(user_id)
    assert result == expected
    mock_repository.get_by_user.assert_called_once_with(user_id)

def test_get_by_user_and_date(service, mock_repository):
    user_id = uuid4()
    test_date = date.today()
    expected = [make_shift()]
    mock_repository.get_by_user_and_date.return_value = expected
    result = service.get_by_user_and_date(user_id, test_date)
    assert result == expected
    mock_repository.get_by_user_and_date.assert_called_once_with(user_id, test_date)

def test_update_success(service, mock_repository):
    shift_id = uuid4()
    data = {"note": "updated"}
    expected = make_shift()
    mock_repository.update.return_value = expected
    result = service.update(shift_id, data)
    assert result == expected
    mock_repository.update.assert_called_once_with(shift_id, data)

def test_update_not_found(service, mock_repository):
    shift_id = uuid4()
    data = {"note": "updated"}
    mock_repository.update.side_effect = ValueError
    with pytest.raises(ValueError):
        service.update(shift_id, data)

def test_get_shift_types(service, mock_repository):
    expected = [make_shift_type()]
    mock_repository.get_shift_types.return_value = expected
    result = service.get_shift_types()
    assert result == expected
    mock_repository.get_shift_types.assert_called_once()