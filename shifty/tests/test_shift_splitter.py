from datetime import date, time, datetime
from uuid import uuid4
from shifty.domain.entities import Shift, Override, ShiftStatus
from shifty.application.use_cases.shift_splitter import split_shift_for_partial_override

def test_split_shift_for_partial_override():
    shift = Shift(
        id=uuid4(),
        user_id=uuid4(),
        origin_user_id=uuid4(),
        organization_id=uuid4(),
        date=date(2025, 6, 18),
        start_time=time(9, 0),
        end_time=time(13, 0),
        status=ShiftStatus.PENDING,
        parent_shift_id=None,
        created_at=datetime.now()
    )
    override = Override(
        id=uuid4(),
        shift_id=shift.id,
        organization_id=shift.organization_id,
        user_id=shift.user_id,
        date=shift.date,
        start_time=time(9, 0),
        end_time=time(13, 0),
        taken_by_id=None,
        taken_at=None,
        created_at=datetime.now(),
        is_taken=False
    )
    taker_user_id = uuid4()
    segments = split_shift_for_partial_override(
        shift, override, time(10, 0), time(12, 0), taker_user_id
    )
    assert len(segments) == 3
    assert segments[0].start_time == time(9, 0)
    assert segments[0].end_time == time(10, 0)
    assert segments[0].user_id == shift.user_id
    assert segments[1].start_time == time(10, 0)
    assert segments[1].end_time == time(12, 0)
    assert segments[1].user_id == taker_user_id
    assert segments[1].status == ShiftStatus.TAKEN
    assert segments[2].start_time == time(12, 0)
    assert segments[2].end_time == time(13, 0)
    assert segments[2].user_id == shift.user_id