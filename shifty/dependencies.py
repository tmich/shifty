from fastapi import Depends
from shifty.application.use_cases.availability_service import AvailabilityService
from shifty.application.use_cases.shift_service import ShiftService
from shifty.infrastructure.repositories.availability_sqlalchemy import AvailabilityRepository
from shifty.infrastructure.db import get_session
from shifty.infrastructure.repositories.shift_sqlalchemy import ShiftRepository
from shifty.infrastructure.repositories.user_sqlalchemy import UserRepository

def get_availability_service(session = Depends(get_session)) -> AvailabilityService:
    repository = AvailabilityRepository(session)
    return AvailabilityService(repository)

def get_shift_service(session=Depends(get_session)):
    return ShiftService(
        ShiftRepository(session),
        AvailabilityRepository(session),
        UserRepository(session)
    )