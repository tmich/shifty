import uuid
from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional
from shifty.domain.entities import Availability, User
from shifty.application.dto.dto import ApiResult


class AvailabilityCreate(BaseModel):
    user_id: uuid.UUID
    organization_id: uuid.UUID
    date: date
    start_time: time
    end_time: time
    note: Optional[str] = None
    created_at: datetime = datetime.now()  # Assuming this is set automatically when creating an availability


class AvailabilityResult(ApiResult):
    """
    Represents the result of an availability operation.
    This class can be extended to include more details about the operation if needed.
    """
    kind: str = "Availability"
    availability: Availability | None = None  # The availability object if the operation was successful


class AvailabilityFull(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    organization_id: uuid.UUID
    date: date
    start_time: time
    end_time: time
    note: Optional[str] = None
    created_at: datetime
    user: Optional[User]

    class Config:
        orm_mode = True  # This allows the model to work with ORM objects directly