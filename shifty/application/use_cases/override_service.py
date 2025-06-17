from uuid import UUID
from typing import List
from datetime import datetime
from shifty.domain.entities import Override
from shifty.application.dto.override_dto import OverrideCreate
from shifty.infrastructure.repositories.override_sqlalchemy import OverrideRepository
from shifty.infrastructure.repositories.shift_sqlalchemy import ShiftRepository
from shifty.domain.exceptions import InvalidOverrideException

class OverrideService:
    def __init__(self, override_repository: OverrideRepository, shift_repository: ShiftRepository):
        self.override_repository = override_repository
        self.shift_repository = shift_repository

    def create(self, data: OverrideCreate) -> Override:
        # Fetch the shift
        shift = self.shift_repository.get_by_id(data.shift_id)
        if not shift:
            raise InvalidOverrideException("Referenced shift does not exist.")

        # Business rule: date must match
        if data.date != shift.date:
            raise InvalidOverrideException("Override date must match shift date.")

        # Business rule: time range must be within shift's time range
        if not (shift.start_time <= data.start_time < data.end_time <= shift.end_time):
            raise InvalidOverrideException("Override time range must be within shift's time range.")

        # NEW RULE: No overlapping overrides for the same shift
        existing_overrides = self.override_repository.get_all()
        for o in existing_overrides:
            if o.shift_id == data.shift_id and o.date == data.date:
                # Check for time overlap
                if not (data.end_time <= o.start_time or data.start_time >= o.end_time):
                    raise InvalidOverrideException("Cannot create overlapping override for the same shift.")

        override = Override(
            shift_id=data.shift_id,
            requester_id=data.requester_id,
            date=data.date,
            start_time=data.start_time,
            end_time=data.end_time,
            created_at=datetime.now(),
            is_taken=False
        )
        return self.override_repository.add(override)

    def list_all(self) -> List[Override]:
        return self.override_repository.get_all()

    def get_by_id(self, override_id: UUID) -> Override:
        override = self.override_repository.get_by_id(override_id)
        if not override:
            raise ValueError("Override not found")
        return override

    def list_open(self) -> List[Override]:
        return self.override_repository.get_open()

    def take(self, override_id: UUID, taken_by_id: UUID) -> Override:
        override = self.override_repository.get_by_id(override_id)
        repr(override)
        if not override:
            print(f"Override {override_id} not found.")
            raise InvalidOverrideException("Override not available.")
        
        if override.is_taken:
            print(f"Override {override_id} is already taken by {override.taken_by_id}.")
            raise InvalidOverrideException("Override already taken.")

        # Fetch the shift to check the owner
        shift = self.shift_repository.get_by_id(override.shift_id)
        if not shift:
            raise InvalidOverrideException("Associated shift not found.")

        # Business rule: taker cannot be the shift owner
        if shift.user_id == taken_by_id:
            raise InvalidOverrideException("Shift owner cannot take their own override.")

        return self.override_repository.take(override_id, taken_by_id)