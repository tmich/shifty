import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import date, time, datetime

from shifty.application.use_cases.override_service import OverrideService
from shifty.application.dto.override_dto import OverrideCreate, OverrideTake, OverrideUpdate
from shifty.domain.entities import Override, Shift, ShiftStatus

@pytest.fixture
def mock_shift_repository():
    return MagicMock()

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def mock_override_repository():
    return MagicMock()

@pytest.fixture
def service(mock_repository, mock_shift_repository):
    # Provide mock_repository for both override_repository and shift_repository
    return OverrideService(mock_repository, mock_shift_repository)

def make_override():
    return Override(
        id=uuid4(),
        shift_id=uuid4(),
        requester_id=uuid4(),
        date=date(2025, 6, 17),
        start_time=time(9, 0),
        end_time=time(17, 0),
        taken_by_id=None,
        taken_at=None,
        created_at=datetime.now(),
        is_taken=False
    )

def make_shift():
    user_id = uuid4()
    return Shift(
        id=user_id,
        user_id=uuid4(),
        parent_shift_id=None,
        organization_id=uuid4(),
        date=date(2025, 6, 17),
        start_time=time(9, 0),
        end_time=time(17, 0),
        origin_user_id=user_id,
        note="Test shift",
        created_at=datetime.now()
    )

def make_create_dto():
    return OverrideCreate(
        shift_id=uuid4(),
        requester_id=uuid4(),
        date=date(2025, 6, 17),
        start_time=time(9, 0),
        end_time=time(17, 0)
    )

def test_create_success(service, mock_repository, mock_shift_repository):
    dto = make_create_dto()
    expected = make_override()
    mock_repository.add.return_value = expected
    mock_shift_repository.get_by_id.return_value = make_shift()  # Mock the shift retrieval
    result = service.create(dto)
    assert result == expected
    mock_repository.add.assert_called_once()

def test_list_all(service, mock_repository):
    expected = [make_override()]
    mock_repository.get_all.return_value = expected
    result = service.list_all()
    assert result == expected
    mock_repository.get_all.assert_called_once()

def test_get_by_id_success(service, mock_repository):
    expected = make_override()
    mock_repository.get_by_id.return_value = expected
    result = service.get_by_id(expected.id)
    assert result == expected
    mock_repository.get_by_id.assert_called_once_with(expected.id)

def test_get_by_id_not_found(service, mock_repository):
    mock_repository.get_by_id.return_value = None
    with pytest.raises(ValueError):
        service.get_by_id(uuid4())

def test_list_open(service, mock_repository):
    expected = [make_override()]
    mock_repository.get_open.return_value = expected
    result = service.list_open()
    assert result == expected
    mock_repository.get_open.assert_called_once()

def test_take_success(service, mock_repository, mock_shift_repository):
    override_id = uuid4()
    taker_id = uuid4()
    expected = make_override()
    override = make_override()
    override.id = override_id
    mock_repository.get_by_id.return_value = override
    mock_shift_repository.get_by_id.return_value = make_shift()
    service.override_repository = mock_repository
    service.shift_repository = mock_shift_repository
    data = OverrideTake(taken_by_id=taker_id, start_time=time(10, 0), end_time=time(12, 0))
    mock_repository.update.return_value = expected
    result = service.take(override_id, data)
    mock_repository.update.assert_called_once()
    assert result is not None

def test_take_not_available(service, mock_repository, mock_shift_repository):
    override_id = uuid4()
    taker_id = uuid4()
    override = make_override()
    override.id = override_id
    mock_repository.get_by_id.return_value = override
    mock_shift_repository.get_by_id.return_value = make_shift()
    service.override_repository = mock_repository
    service.shift_repository = mock_shift_repository
    data = OverrideTake(taken_by_id=taker_id, start_time=time(10, 0), end_time=time(12, 0))
    mock_repository.update.side_effect = ValueError
    override.is_taken = True  # Simulate already taken
    with pytest.raises(Exception):
        service.take(override_id, data)

def test_create_invalid_date(service, mock_repository):
    # Setup
    dto = make_create_dto()
    shift = make_override()  # Use as a dummy shift
    shift.date = date(2025, 1, 1)
    mock_repository.get_by_id.return_value = shift
    service.shift_repository = mock_repository
    dto.date = date(2025, 1, 2)  # Different date
    with pytest.raises(Exception) as excinfo:
        service.create(dto)
    assert "date must match" in str(excinfo.value)

def test_create_invalid_time(service, mock_repository):
    # Setup
    dto = make_create_dto()
    shift = make_override()
    shift.date = dto.date
    shift.start_time = time(9, 0)
    shift.end_time = time(17, 0)
    mock_repository.get_by_id.return_value = shift
    service.shift_repository = mock_repository
    dto.start_time = time(8, 0)  # Before shift
    dto.end_time = time(18, 0)   # After shift
    with pytest.raises(Exception) as excinfo:
        service.create(dto)
    assert "time range must be within" in str(excinfo.value)

def test_take_by_shift_owner_forbidden(service, mock_repository, mock_shift_repository):
    # Setup
    override_id = uuid4()
    shift_owner_id = uuid4()
    override = make_override()
    override.shift_id = uuid4()
    mock_repository.get_by_id.return_value = override

    shift = make_shift()
    shift.id = override.shift_id
    shift.user_id = shift_owner_id
    mock_shift_repository.get_by_id.return_value = shift

    # Service uses both repositories
    service.override_repository = mock_repository
    service.shift_repository = mock_shift_repository

    # Attempt to take override as the shift owner
    data = OverrideTake(taken_by_id=shift_owner_id, start_time=override.start_time, end_time=override.end_time)
    with pytest.raises(Exception) as excinfo:
        service.take(override_id, data)
    assert "Shift owner cannot take their own override" in str(excinfo.value)

def test_create_overlapping_override_forbidden(service, mock_override_repository, mock_shift_repository):
    dto = make_create_dto()
    shift = make_shift()
    shift.id = dto.shift_id
    shift.date = dto.date
    shift.start_time = time(9, 0)
    shift.end_time = time(17, 0)
    mock_shift_repository.get_by_id.return_value = shift

    # Existing override overlaps with the new one
    existing_override = make_override()
    existing_override.shift_id = dto.shift_id
    existing_override.date = dto.date
    existing_override.start_time = time(10, 0)
    existing_override.end_time = time(12, 0)
    mock_override_repository.get_all.return_value = [existing_override]

    service.override_repository = mock_override_repository
    service.shift_repository = mock_shift_repository

    with pytest.raises(Exception) as excinfo:
        service.create(dto)
    assert "Cannot create overlapping override for the same shift" in str(excinfo.value)

def test_partial_take_splits_shift(service, mock_override_repository, mock_shift_repository):
    # Setup shift and override
    shift = make_shift()
    override = make_override()
    override.shift_id = shift.id
    override.start_time = time(9, 0)
    override.end_time = time(13, 0)
    shift.start_time = time(9, 0)
    shift.end_time = time(13, 0)
    taker_id = uuid4()
    data = OverrideTake(taken_by_id=taker_id, start_time=time(10, 0), end_time=time(12, 0))

    mock_override_repository.get_by_id.return_value = override
    mock_shift_repository.get_by_id.return_value = shift

    service.override_repository = mock_override_repository
    service.shift_repository = mock_shift_repository

    segments = service.take(override.id, data)
    assert len(segments) == 3
    assert segments[1].user_id == taker_id
    assert segments[1].start_time == time(10, 0)
    assert segments[1].end_time == time(12, 0)
    assert segments[1].status == ShiftStatus.TAKEN