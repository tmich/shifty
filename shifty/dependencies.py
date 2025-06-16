from fastapi import Depends, HTTPException, Request, status
import os
import jwt
from shifty.application.use_cases.availability_service import AvailabilityService
from shifty.infrastructure.repositories.availability_sqlalchemy import AvailabilityRepository
from shifty.infrastructure.db import get_session, get_db_with_rls

#def get_availability_service(session = Depends(get_session)) -> AvailabilityService:
def get_availability_service(session = Depends(get_db_with_rls)) -> AvailabilityService:
    repository = AvailabilityRepository(session)
    return AvailabilityService(repository)



