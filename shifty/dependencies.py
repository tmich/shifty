from fastapi import Depends
from shifty.application.use_cases.availability_service import AvailabilityService
from shifty.infrastructure.repositories.availability_sqlalchemy import AvailabilityRepository
from shifty.infrastructure.db import get_session

def get_availability_service(session = Depends(get_session)) -> AvailabilityService:
    repository = AvailabilityRepository(session)
    return AvailabilityService(repository)