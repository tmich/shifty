from uuid import UUID
from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional


class AvailabilityCreate(BaseModel):
    user_id: UUID
    date: date
    start_time: time
    end_time: time
    note: Optional[str] = None


class AvailabilityRead(BaseModel):
    id: UUID
    user_id: UUID
    date: date
    start_time: time
    end_time: time
    note: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True  # permette di usare gli attributi del modello SQLAlchemy direttamente
