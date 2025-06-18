from datetime import date, time
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from shifty.domain.entities import ShiftType, ShiftBase, User


class ShiftCreate(BaseModel):
    user_id: UUID
    origin_user_id: UUID
    organization_id: UUID
    date: date
    start_time: time
    end_time: time
    note: Optional[str] = None


class ShiftCalculationRequest(BaseModel):
    date: date
    organization_id: UUID


class ShiftCalculationResult(ShiftBase):
    shift_type: Optional[ShiftType] = None
    user: User | None = None

