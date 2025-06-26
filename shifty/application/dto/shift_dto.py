from datetime import date, time, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from shifty.domain.entities import ShiftSlot, ShiftBase, User


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
    shift_type: Optional[ShiftSlot] = None
    user: User | None = None


class ShiftSlotOut(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    start_time: time
    end_time: time
    description: Optional[str] = None
    expected_workers: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True


class ShiftBulkCreate(BaseModel):
    shifts: list[ShiftCreate]


class ShiftSlotCreate(BaseModel):
    organization_id: UUID
    name: str
    start_time: time
    end_time: time
    description: Optional[str] = None
    expected_workers: int = 1
    is_active: bool = True


class ShiftSlotUpdate(BaseModel):
    name: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    description: Optional[str] = None
    expected_workers: Optional[int] = None
    is_active: Optional[bool] = None
