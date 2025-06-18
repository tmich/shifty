from uuid import UUID
from datetime import datetime
from typing import List
from shifty.domain.entities import Shift, ShiftStatus
from shifty.domain.exceptions import OverlappingShiftException, NotExistsException
from shifty.application.dto.shift_dto import ShiftCreate
from shifty.infrastructure.repositories.shift_sqlalchemy import ShiftRepository

class ShiftService:
    def __init__(self, repository: ShiftRepository):
        self.repository = repository

    def create(self, data: ShiftCreate) -> Shift:
        # Business rule: cannot create overlapping shifts for the same owner
        existing_shifts = self.repository.get_by_user_and_date(data.user_id, data.date)
        for s in existing_shifts:
            if not (data.end_time <= s.start_time or data.start_time >= s.end_time):
                raise OverlappingShiftException("Cannot create overlapping shift for the same owner.")
            
        shift = Shift(
            user_id=data.user_id,
            # parent_shift_id=data.parent_shift_id,
            origin_user_id=data.origin_user_id,
            organization_id=data.organization_id,
            date=data.date,
            start_time=data.start_time,
            end_time=data.end_time,
            note=data.note,
            status=ShiftStatus.TAKEN,  # Default status
            created_at=datetime.now()
        )
        return self.repository.add(shift)

    def list_all(self) -> List[Shift]:
        return self.repository.get_all()

    def get_by_id(self, shift_id: UUID) -> Shift:
        shift = self.repository.get_by_id(shift_id)
        if not shift:
            raise ValueError("Shift not found")
        return shift

    def delete(self, shift_id: UUID) -> None:
        try:
            self.repository.delete(shift_id)
        except ValueError:
            raise ValueError("Shift not found")

    def get_by_date(self, date):
        return self.repository.get_by_date(date)

    def get_by_user(self, user_id):
        return self.repository.get_by_user(user_id)

    def get_by_user_and_date(self, user_id, date):
        return self.repository.get_by_user_and_date(user_id, date)

    def update(self, shift_id, data):
        try:
            return self.repository.update(shift_id, data)
        except ValueError:
            raise NotExistsException("Shift not found")