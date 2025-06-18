from datetime import date, time, datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel

if TYPE_CHECKING:
    from datetime import date, time

class OverrideCreate(BaseModel):
    shift_id: UUID
    requester_id: UUID
    date: date
    start_time: time
    end_time: time

class OverrideRead(BaseModel):
    id: UUID
    shift_id: UUID
    requester_id: UUID
    date: date
    start_time: time
    end_time: time
    taken_by_id: Optional[UUID]
    taken_at: Optional[datetime]
    created_at: datetime
    is_taken: bool

class OverrideTake(BaseModel):
    taken_by_id: UUID
    start_time: time
    end_time: time

class OverrideUpdate(BaseModel):
    shift_id: Optional[UUID] = None
    requester_id: Optional[UUID] = None
    date: date
    start_time: time
    end_time: time
    taken_by_id: Optional[UUID] = None
    taken_at: Optional[datetime] = None
    is_taken: Optional[bool] = None