import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import date, time, datetime

from shifty.application.use_cases.availability_service import AvailabilityService, InvalidDateRangeException, NotExistsException
from shifty.application.dto.availability_dto import AvailabilityCreate
from shifty.domain.entities import Availability

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def service(mock_repository):
    return AvailabilityService(mock_repository)

def make_availability():
    return Availability(
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
    return AvailabilityCreate(
        user_id=uuid4(),
        organization_id=uuid4(),
        date=date.today(),
        start_time=time(9, 0),
        end_time=time(17, 0),
        note="test"
    )

def test_create_success(service, mock_repository):
    dto = make_create_dto()
    expected = make_availability()
    mock_repository.add.return_value = expected
    result = service.create(dto)
    assert result == expected
    mock_repository.add.assert_called_once()

def test_create_invalid_time(service):
    dto = make_create_dto()
    dto.start_time = time(18, 0)
    dto.end_time = time(9, 0)
    with pytest.raises(InvalidDateRangeException):
        service.create(dto)

def test_list_all(service, mock_repository):
    expected = [make_availability()]
    mock_repository.get_all.return_value = expected
    result = service.list_all()
    assert result == expected
    mock_repository.get_all.assert_called_once()

def test_delete_success(service, mock_repository):
    service.delete(uuid4())
    mock_repository.delete.assert_called_once()

def test_delete_not_exists(service, mock_repository):
    mock_repository.delete.side_effect = ValueError
    with pytest.raises(NotExistsException):
        service.delete(uuid4())

def test_get_by_id_success(service, mock_repository):
    expected = make_availability()
    mock_repository.get_by_id.return_value = expected
    result = service.get_by_id(expected.id)
    assert result == expected
    mock_repository.get_by_id.assert_called_once_with(expected.id)

def test_get_by_id_not_exists(service, mock_repository):
    mock_repository.get_by_id.side_effect = ValueError
    with pytest.raises(NotExistsException):
        service.get_by_id(uuid4())

def test_get_by_user_id_success(service, mock_repository):
    user_id = uuid4()
    availabilities = [make_availability(), make_availability()]
    mock_repository.get_by_user_id.return_value = availabilities
    result = service.get_by_user_id(user_id)
    assert result == availabilities
    mock_repository.get_by_user_id.assert_called_once_with(user_id)

def test_get_by_user_id_empty(service, mock_repository):
    user_id = uuid4()
    mock_repository.get_by_user_id.return_value = []
    result = service.get_by_user_id(user_id)
    assert result == []
    mock_repository.get_by_user_id.assert_called_once_with(user_id)

def test_update_calls_repository_update(service, mock_repository):
    availability = make_availability()
    service.update(availability.id, availability)
    mock_repository.update.assert_called_once_with(availability.id, availability)

def test_get_by_user_id_and_date_success(service, mock_repository):
    user_id = uuid4()
    test_date = date.today()
    availabilities = [make_availability(), make_availability()]
    mock_repository.get_by_user_id_and_date.return_value = availabilities
    result = service.get_by_user_id_and_date(user_id, test_date)
    assert result == availabilities
    mock_repository.get_by_user_id_and_date.assert_called_once_with(user_id, test_date)

def test_get_by_date_success(service, mock_repository):
    test_date = date.today()
    availabilities = [make_availability(), make_availability()]
    mock_repository.get_by_date.return_value = availabilities
    result = service.get_by_date(test_date)
    assert result == availabilities
    mock_repository.get_by_date.assert_called_once_with(test_date)

def test_get_by_date_empty(service, mock_repository):
    test_date = date.today()
    mock_repository.get_by_date.return_value = []
    result = service.get_by_date(test_date)
    assert result == []
    mock_repository.get_by_date.assert_called_once_with(test_date)

def test_get_by_user_id_and_date_empty(service, mock_repository):
    user_id = uuid4()
    test_date = date.today()
    mock_repository.get_by_user_id_and_date.return_value = []
    result = service.get_by_user_id_and_date(user_id, test_date)
    assert result == []
    mock_repository.get_by_user_id_and_date.assert_called_once_with(user_id, test_date)

def test_create_overlapping_availability_raises(service, mock_repository):
    dto = make_create_dto()
    # Existing availability overlaps with new one
    existing = Availability(
        id=uuid4(),
        user_id=dto.user_id,
        organization_id=dto.organization_id,
        date=dto.date,
        start_time=time(8, 0),
        end_time=time(12, 0),
        note="existing",
        created_at=datetime.now()
    )
    mock_repository.get_by_user_id_and_date.return_value = [existing]
    dto.start_time = time(11, 0)
    dto.end_time = time(13, 0)
    with pytest.raises(Exception) as excinfo:
        service.create(dto)
    assert "overlaps" in str(excinfo.value)

def test_create_past_date_raises(service):
    dto = make_create_dto()
    dto.date = date(2000, 1, 1)
    with pytest.raises(InvalidDateRangeException):
        service.create(dto)

def test_update_calls_repository_update_with_correct_availability(service, mock_repository):
    availability = make_availability()
    service.update(availability.id, availability)
    mock_repository.update.assert_called_with(availability.id, availability)

def test_delete_raises_not_exists_exception(service, mock_repository):
    mock_repository.delete.side_effect = ValueError("not found")
    with pytest.raises(NotExistsException):
        service.delete(uuid4())

def test_get_by_id_raises_not_exists_exception(service, mock_repository):
    mock_repository.get_by_id.side_effect = ValueError("not found")
    with pytest.raises(NotExistsException):
        service.get_by_id(uuid4())

def test_get_by_user_id_and_date_with_no_results(service, mock_repository):
    user_id = uuid4()
    test_date = date.today()
    mock_repository.get_by_user_id_and_date.return_value = []
    result = service.get_by_user_id_and_date(user_id, test_date)
    assert result == []
    mock_repository.get_by_user_id_and_date.assert_called_with(user_id, test_date)

def test_get_by_date_with_no_results(service, mock_repository):
    test_date = date.today()
    mock_repository.get_by_date.return_value = []
    result = service.get_by_date(test_date)
    assert result == []
    mock_repository.get_by_date.assert_called_with(test_date)
