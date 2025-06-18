from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from shifty.domain.entities import Shift, ShiftType
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

    def get_shift_types(self) -> List[ShiftType]:
        return list(self.session.exec(select(ShiftType)).all())