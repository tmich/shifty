from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from datetime import datetime

from shifty.application.dto.override_dto import OverrideUpdate
from shifty.domain.entities import Override

class OverrideRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, override: Override) -> Override:
        self.session.add(override)
        self.session.commit()
        self.session.refresh(override)
        return override

    def get_all(self) -> List[Override]:
        return list(self.session.exec(select(Override)).all())

    def get_by_id(self, override_id: UUID) -> Optional[Override]:
        return self.session.get(Override, override_id)

    def get_open(self) -> List[Override]:
        return list(self.session.exec(select(Override).where(Override.is_taken == False)).all())
    


    def take(self, override_id: UUID, taken_by_id: UUID) -> Override:
        override = self.session.get(Override, override_id)
        if not override or override.is_taken:
            raise ValueError("Override not available")
        override.taken_by_id = taken_by_id
        override.taken_at = datetime.now()
        override.is_taken = True
        self.session.add(override)
        self.session.commit()
        self.session.refresh(override)
        return override

    def update(self, override_id: UUID, data: OverrideUpdate) -> Override:
        """
        Update an existing Override entity.
        :param override_id: UUID of the override to update.
        :param data: dict or Pydantic model with fields to update.
        :return: Updated Override instance.
        """
        override = self.session.get(Override, override_id)
        if not override:
            raise ValueError(f"Override with id {override_id} does not exist.")

        update_data = data.model_dump(exclude_unset=True)
        override.sqlmodel_update(update_data)
        self.session.add(override)
        self.session.commit()
        self.session.refresh(override)
        return override
    