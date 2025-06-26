from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from shifty.domain.entities import Shift, ShiftSlot
from shifty.domain.repositories import ShiftRepositoryInterface


class ShiftRepository(ShiftRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def add(self, shift: Shift) -> Shift:
        self.session.add(shift)
        self.session.commit()
        self.session.refresh(shift)
        return shift

    def get_all(self) -> List[Shift]:
        return list(self.session.exec(select(Shift)).all())

    def get_by_id(self, shift_id: UUID) -> Optional[Shift]:
        return self.session.get(Shift, shift_id)

    def delete(self, shift_id: UUID) -> None:
        shift = self.session.get(Shift, shift_id)
        if shift:
            self.session.delete(shift)
            self.session.commit()
        else:
            raise ValueError("Shift not found")

    def get_by_date(self, date) -> List[Shift]:
        return list(self.session.exec(select(Shift).where(Shift.date == date)).all())

    def get_by_user(self, user_id) -> List[Shift]:
        return list(self.session.exec(select(Shift).where(Shift.user_id == user_id)).all())

    def get_by_user_and_date(self, user_id, date) -> List[Shift]:
        return list(self.session.exec(
            select(Shift).where(Shift.user_id == user_id, Shift.date == date)
        ).all())

    def update(self, shift_id, data) -> Shift:
        shift = self.session.get(Shift, shift_id)
        if not shift:
            raise ValueError("Shift not found")
        for field, value in data.items():
            setattr(shift, field, value)
        self.session.add(shift)
        self.session.commit()
        self.session.refresh(shift)
        return shift

    def get_shift_slots(self) -> List[ShiftSlot]:
        return list(self.session.exec(select(ShiftSlot)).all())

    def get_shift_slots_by_organization(self, organization_id: UUID) -> List[ShiftSlot]:
        return list(self.session.exec(
            select(ShiftSlot).where(ShiftSlot.organization_id == organization_id)
        ).all())

    def add_shift_slot(self, shift_slot: ShiftSlot) -> ShiftSlot:
        self.session.add(shift_slot)
        self.session.commit()
        self.session.refresh(shift_slot)
        return shift_slot

    def update_shift_slot(self, shift_slot_id: UUID, data: dict) -> ShiftSlot:
        shift_slot = self.session.get(ShiftSlot, shift_slot_id)
        if not shift_slot:
            raise ValueError("Shift slot not found")
        for field, value in data.items():
            setattr(shift_slot, field, value)
        self.session.add(shift_slot)
        self.session.commit()
        self.session.refresh(shift_slot)
        return shift_slot

    def delete_shift_slot(self, shift_slot_id: UUID) -> None:
        shift_slot = self.session.get(ShiftSlot, shift_slot_id)
        if shift_slot:
            self.session.delete(shift_slot)
            self.session.commit()
        else:
            raise ValueError("Shift slot not found")

    def get_shift_slot_by_id(self, shift_slot_id: UUID) -> Optional[ShiftSlot]:
        return self.session.get(ShiftSlot, shift_slot_id)
