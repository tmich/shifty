from datetime import datetime, time
from uuid import UUID, uuid4
from typing import List
from shifty.domain.entities import Shift, Override, ShiftStatus

def split_shift_for_partial_override(
    shift: Shift,
    override: Override,
    claimed_start: time,
    claimed_end: time,
    taker_user_id: UUID
) -> List[Shift]:
    """
    Splits the shift into up to three segments:
    - before the claimed range (if any)
    - the claimed range (assigned to taker)
    - after the claimed range (if any)
    All new segments reference the original shift via parent_shift_id.
    """
    segments = []
    # Before claimed
    if shift.start_time < claimed_start:
        segments.append(Shift(
            id=uuid4(),
            user_id=shift.user_id,
            origin_user_id=shift.origin_user_id,
            organization_id=shift.organization_id,
            date=shift.date,
            start_time=shift.start_time,
            end_time=claimed_start,
            status=shift.status,
            parent_shift_id=shift.id,
            note=shift.note,
            created_at=datetime.now()
        ))
    # Claimed segment
    segments.append(Shift(
        id=uuid4(),
        user_id=taker_user_id,
        origin_user_id=shift.origin_user_id,
        organization_id=shift.organization_id,
        date=shift.date,
        start_time=claimed_start,
        end_time=claimed_end,
        status=ShiftStatus.TAKEN,
        parent_shift_id=shift.id,
        note=f"Taken via override {override.id}",
        created_at=datetime.now()
    ))
    # After claimed
    if claimed_end < shift.end_time:
        segments.append(Shift(
            id=uuid4(),
            user_id=shift.user_id,
            origin_user_id=shift.origin_user_id,
            organization_id=shift.organization_id,
            date=shift.date,
            start_time=claimed_end,
            end_time=shift.end_time,
            status=shift.status,
            parent_shift_id=shift.id,
            note=shift.note,
            created_at=datetime.now()
        ))
    return segments