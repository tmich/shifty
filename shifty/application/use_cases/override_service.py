from uuid import UUID, uuid4
from typing import List
from datetime import datetime, time
from shifty.domain.entities import Override, Shift, ShiftStatus
from shifty.application.dto.override_dto import OverrideCreate, OverrideTake, OverrideUpdate
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
            user_id=data.requester_id,
            organization_id=shift.organization_id,
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

    def take(self, override_id: UUID, data: OverrideTake) -> List[Shift]:
        override = self.override_repository.get_by_id(override_id)
        if not override:
            raise InvalidOverrideException("Override not available.")
        
        if override.is_taken:
            raise InvalidOverrideException("Override already taken.")

        # Fetch the shift to check the owner
        shift = self.shift_repository.get_by_id(override.shift_id)
        if not shift:
            raise InvalidOverrideException("Associated shift not found.")
        
        # Validate claimed range
        if not (override.start_time <= data.start_time < data.end_time <= override.end_time):
            raise InvalidOverrideException("Claimed range must be within override range.")
        if not (shift.start_time <= data.start_time < data.end_time <= shift.end_time):
            raise InvalidOverrideException("Claimed range must be within shift range.")


        # Business rule: taker cannot be the shift owner
        if shift.user_id == data.taken_by_id:
            raise InvalidOverrideException("Shift owner cannot take their own override.")
        
        # Create the new shifts based on the claimed range
        segments = self.split_shift_for_partial_override(
            shift,
            override,
            data.start_time,
            data.end_time,
            data.taken_by_id
        )
        # Add the new shifts to the repository
        for new_shift in segments:
            self.shift_repository.add(new_shift)

        # Mark override as taken
        override_update = OverrideUpdate(
            shift_id=override.shift_id,
            requester_id=override.user_id,
            date=override.date,
            start_time=data.start_time,
            end_time=data.end_time,
            taken_by_id=data.taken_by_id,
            taken_at=datetime.now(),
            is_taken=True
        )
        # override.taken_by_id = data.taken_by_id
        # override.taken_at = datetime.now()
        # override.is_taken = True
        self.override_repository.update(override_id, override_update)

        # Remove or mark the original shift as canceled (optional: delete or set status)
        self.shift_repository.update(shift.id, {"status": ShiftStatus.CANCELED})
        return segments

    def split_shift_for_partial_override(
        self,
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