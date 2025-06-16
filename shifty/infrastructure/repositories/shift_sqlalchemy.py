from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select

from shifty.domain.entities import Shift

class ShiftRepository:
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