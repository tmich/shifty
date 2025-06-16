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


class AvailabilityUpdate(BaseModel):
    date: date
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    note: Optional[str] = None
    

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

    class ConfigDict:
        from_attributes = True # Allows the model to be created from SQLModel attributes