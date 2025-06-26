from uuid import UUID
from datetime import datetime
from typing import List
from shifty.domain.entities import Shift, ShiftStatus
from shifty.domain.exceptions import OverlappingShiftException, NotExistsException
from shifty.application.dto.shift_dto import ShiftCreate, ShiftCalculationRequest, ShiftCalculationResult
from shifty.domain.repositories import ShiftRepositoryInterface, AvailabilityRepositoryInterface, UserRepositoryInterface
import random
import copy

class ShiftService:
    def __init__(self,
                 repository: ShiftRepositoryInterface,
                 availability_repository: AvailabilityRepositoryInterface,
                 user_repository: UserRepositoryInterface):
        self.repository = repository
        self.availability_repository = availability_repository
        self.user_repository = user_repository

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

    def create_bulk(self, data: list[ShiftCreate]) -> list[Shift]:
        created = []
        for shift_data in data:
            try:
                created_shift = self.create(shift_data)
                created.append(copy.deepcopy(created_shift))
            except Exception as e:
                continue
            # TODO: Handle exceptions for each shift creation
        return created

    def list_all(self) -> List[Shift]:
        return self.repository.get_all()

    def get_by_id(self, shift_id: UUID) -> Shift:
        shift = self.repository.get_by_id(shift_id)
        if not shift:
            raise NotExistsException("Shift not found")
        return shift

    def delete(self, shift_id: UUID) -> None:
        try:
            self.repository.delete(shift_id)
        except ValueError:
            raise NotExistsException("Shift not found")

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

    def get_shift_slots(self):
        return self.repository.get_shift_slots()

    def calculate_shifts(self, request: ShiftCalculationRequest) -> list[ShiftCalculationResult]:
        availabilities = self.availability_repository.get_by_date(request.date)
        shift_slots = self.repository.get_shift_slots()
        assigned_users = set()
        results = []
        all_users = [u.id for u in self.user_repository.get_by_role("worker")]
        for shift_slot in shift_slots:
            shift_start = shift_slot.start_time
            shift_end = shift_slot.end_time
            needed = getattr(shift_slot, 'expected_workers', 1)
            assigned_for_this_shift = 0
            # Try to cover the shift with available users (no user can do more than one shift)
            for a in availabilities:
                if a.user_id in assigned_users:
                    continue
                if a.start_time <= shift_start and a.end_time >= shift_end:
                    assigned_users.add(a.user_id)
                    results.append(ShiftCalculationResult(
                        user_id=a.user_id,
                        organization_id=request.organization_id,
                        date=request.date,
                        created_at=datetime.now(),
                        shift_type=shift_slot,
                        start_time=shift_start,
                        end_time=shift_end,
                        user=self.user_repository.get_by_id(a.user_id)
                    ))
                    assigned_for_this_shift += 1
                    if assigned_for_this_shift >= needed:
                        break
            # If not enough, pick random users not already assigned
            while assigned_for_this_shift < needed:
                available_users = [u for u in all_users if u not in assigned_users]
                if not available_users:
                    break
                chosen_user_id = random.choice(available_users)
                results.append(ShiftCalculationResult(
                    user_id=chosen_user_id,
                    organization_id=request.organization_id,
                    date=request.date,
                    created_at=datetime.now(),
                    shift_type=shift_slot,
                    start_time=shift_start,
                    end_time=shift_end,
                    user=self.user_repository.get_by_id(chosen_user_id)
                ))
                assigned_users.add(chosen_user_id)
                assigned_for_this_shift += 1
        return results
