import os
import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import date, time, datetime

from shifty.application.use_cases.shift_service import ShiftService
from shifty.application.dto.shift_dto import ShiftCreate, ShiftCalculationRequest, ShiftCalculationResult
from shifty.domain.entities import Availability, Shift, ShiftType
from shifty.domain.exceptions import NotExistsException

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def mock_availability_repository():
    return MagicMock()

@pytest.fixture
def mock_user_repository():
    return MagicMock()

@pytest.fixture
def service(mock_repository, mock_availability_repository, mock_user_repository):
    return ShiftService(
        mock_repository,
        mock_availability_repository,
        mock_user_repository
    )

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

def make_availability(user_id, org_id, date, start, end, note):
    import uuid
    from datetime import datetime
    return Availability(
        id=uuid.uuid4(),
        user_id=user_id,
        organization_id=org_id,
        date=date,
        start_time=start,
        end_time=end,
        note=note,
        created_at=datetime.now()
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
    with pytest.raises(NotExistsException):
        service.get_by_id(uuid4())

def test_delete_success(service, mock_repository):
    service.delete(uuid4())
    mock_repository.delete.assert_called_once()

def test_delete_not_found(service, mock_repository):
    mock_repository.delete.side_effect = ValueError
    with pytest.raises(NotExistsException):
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
    with pytest.raises(NotExistsException):
        service.update(shift_id, data)

def test_get_shift_types(service, mock_repository):
    expected = [make_shift_type()]
    mock_repository.get_shift_types.return_value = expected
    result = service.get_shift_types()
    assert result == expected
    mock_repository.get_shift_types.assert_called_once()

def test_calculate_shifts(service, mock_availability_repository, mock_user_repository, mock_repository):
    from datetime import date, time
    org_id = uuid4()
    user1 = uuid4()
    user2 = uuid4()
    user3 = uuid4()
    user4 = uuid4()
    user5 = uuid4()
    user6 = uuid4()
    availabilities = [
        make_availability(user1, org_id, date.today(), time(8,0), time(12,0), "Morning"),
        make_availability(user2, org_id, date.today(), time(12,0), time(16,0), "Afternoon"),
    ]

    mock_shift_types = [
        ShiftType(
            id=uuid4(),
            organization_id=org_id,
            name="Morning",
            start_time=time(8, 0),
            end_time=time(12, 0),
            description="Morning shift",
            is_active=True,
            created_at=datetime.now(),
            updated_at=None
        ),
        ShiftType(
            id=uuid4(),
            organization_id=org_id,
            name="Afternoon",
            start_time=time(12, 0),
            end_time=time(16, 0),
            description="Afternoon shift",
            is_active=True,
            created_at=datetime.now(),
            updated_at=None
        ),
        ShiftType(
            id=uuid4(),
            organization_id=org_id,
            name="Evening",
            start_time=time(16, 0),
            end_time=time(20, 0),
            description="Evening shift",
            is_active=True,
            created_at=datetime.now(),
            updated_at=None
        )
    ]

    # Mocking the repository to return the shift types
    mock_repository.get_shift_types.return_value = mock_shift_types

    # Mocking the availability repository to return the availabilities
    mock_availability_repository.get_by_date.return_value = availabilities

    # Mocking the user repository to return a list of users
    mock_user_repository.get_by_role.return_value = [
        type('U', (), {"id": user1})(),
        type('U', (), {"id": user2})(),
        type('U', (), {"id": user3})(),
        type('U', (), {"id": user4})(),
        type('U', (), {"id": user5})(),
        type('U', (), {"id": user6})(),
    ]

    # Mocking the user repository to return user details by ID
    mock_user_repository.get_by_id.side_effect = lambda user_id: type('U', (), {
        "id": user_id, 
        "full_name": f"User {user_id}", 
        "email" : "test@test.com", 
        "role": "worker", 
        "organization_id": org_id})()

    req = ShiftCalculationRequest(
        date=date.today(),
        organization_id=org_id,
    )

    result = service.calculate_shifts(req)
    # Should return at least a ShiftCalculationResult for each shift type
    assert len(result) >= len(mock_shift_types)
    shift_type_names = [r.shift_type.name for r in result]
    assert set(shift_type_names) == {"Morning", "Evening", "Afternoon"}
    # Each user gets at most one shift
    user_ids = [r.user_id for r in result]
    assert len(set(user_ids)) == len(user_ids) or len(set(user_ids)) == 2
    # Each result covers the correct time
    for r in result:
        st = next(st for st in mock_repository.get_shift_types.return_value if st.name == r.shift_type.name)
        assert r.start_time == st.start_time
        assert r.end_time == st.end_time