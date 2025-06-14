from uuid import UUID
from datetime import date, time
from fastapi import APIRouter, Depends, Response, status
from shifty.application.dto.availability_dto import AvailabilityCreate, AvailabilityFull, AvailabilityResult
from shifty.application.use_cases.availability_service import AvailabilityService
from shifty.dependencies import get_availability_service
from shifty.domain.entities import Availability  # Updated import
from shifty.domain.exceptions import InvalidDateRangeException, NotExistsException, InvalidAvailabilityException

router = APIRouter(prefix="/availabilities", tags=["availabilities"])

@router.post("/", response_model=AvailabilityResult, status_code=201)
def create_availability(
    data: AvailabilityCreate,
    response: Response,
    service: AvailabilityService = Depends(get_availability_service)
):
    try:
        saved = service.create(data)
        return AvailabilityResult(
            result="success",
            message="Availability created successfully.",
            availability=saved
        )
    except (InvalidDateRangeException, InvalidAvailabilityException) as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return AvailabilityResult(
            result="error",
            message=str(ex),
        )
        

@router.get("/", response_model=list[Availability])
def list_availabilities(
    service: AvailabilityService = Depends(get_availability_service)
):
    return service.list_all()

@router.delete("/{availability_id}", status_code=204)
def delete_availability(
    availability_id: UUID,
    response: Response,
    service: AvailabilityService = Depends(get_availability_service)
):
    try:
        service.delete(availability_id)
    except NotExistsException:
        response.status_code = status.HTTP_404_NOT_FOUND

@router.get("/{availability_id}", response_model=Availability|None)
def get_availability(
    availability_id: UUID,
    response: Response,
    service: AvailabilityService = Depends(get_availability_service)
):
    try:
        return service.get_by_id(availability_id)
    except NotExistsException:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

@router.put("/{availability_id}", response_model=Availability)
def update_availability(
    availability_id: UUID,
    data: AvailabilityCreate,
    service: AvailabilityService = Depends(get_availability_service)
):
    availability = Availability(
        id=availability_id,
        user_id=data.user_id,
        organization_id=data.organization_id,  # Assuming this is part of the DTO
        date=data.date,
        start_time=data.start_time,
        end_time=data.end_time,
        note=data.note,  # Assuming note is optional and can be None
        created_at=data.created_at,  # Assuming created_at is part of the DTO
    )
    service.update(availability)
    return service.get_by_id(availability_id)

@router.get("/user/{user_id}", response_model=list[Availability])
def get_availabilities_by_user(
    user_id: UUID,
    response: Response,
    service: AvailabilityService = Depends(get_availability_service)
):
    availabilities_by_user = service.get_by_user_id(user_id)
    if not availabilities_by_user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return []
    return availabilities_by_user

@router.get("/user/{user_id}/date/{date}", response_model=list[Availability])
def get_availabilities_by_user_and_date(
    user_id: UUID,
    date: date,  # Assuming date is passed as a string in 'YYYY-MM-DD' format
    response: Response,
    service: AvailabilityService = Depends(get_availability_service)
):
    try:
        availabilities = service.get_by_user_id_and_date(user_id, date)
        if not availabilities:
            response.status_code = status.HTTP_404_NOT_FOUND
            return []
        return availabilities
    except ValueError as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"result": "error", "message": str(ex)}
    
@router.get("/date/{date}", response_model=list[AvailabilityFull])
def get_availabilities_by_date(
    date: date,  # Assuming date is passed as a string in 'YYYY-MM-DD' format
    response: Response,
    service: AvailabilityService = Depends(get_availability_service)
):
    availabilities = service.get_by_date(date)
    if not availabilities:
        response.status_code = status.HTTP_404_NOT_FOUND
        return []
    return availabilities