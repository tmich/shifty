from uuid import UUID
from datetime import date, time
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from shifty.application.dto.availability_dto import AvailabilityCreate, AvailabilityFull, AvailabilityResult, AvailabilityUpdate
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
        

@router.get("/", response_model=list[AvailabilityFull])
def list_availabilities(
    service: AvailabilityService = Depends(get_availability_service),
):
    return service.list_all()

@router.delete("/{availability_id}", status_code=204)
def delete_availability(
    availability_id: UUID,
    response: Response,
    service: AvailabilityService = Depends(get_availability_service)
):
    """
    Deletes an availability with the given ID.
    
    Args:
        availability_id: UUID of the availability to delete
        
    Returns:
        204 No Content if successful
        404 Not Found if the availability does not exist
    """
    try:
        service.delete(availability_id)
    except NotExistsException:
        response.status_code = status.HTTP_404_NOT_FOUND

@router.get("/{availability_id}", response_model=AvailabilityFull|None)
def get_availability(
    availability_id: UUID,
    response: Response,
    service: AvailabilityService = Depends(get_availability_service)
):
    try:
        return service.get_by_id(availability_id)
    except NotExistsException:
        raise HTTPException(status_code=404, detail="Availability not found")

@router.put("/{availability_id}", response_model=AvailabilityFull)
def update_availability(
    availability_id: UUID,
    data: AvailabilityUpdate,
    service: AvailabilityService = Depends(get_availability_service)
):
    try:
        return service.update(availability_id, data)
    except NotExistsException:
        raise HTTPException(status_code=404, detail="Availability not found")
    

@router.get("/user/{user_id}", response_model=list[AvailabilityFull])
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

@router.get("/user/{user_id}/date/{date}", response_model=list[AvailabilityFull])
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

@router.options("/")
def options_availabilities():
    return Response(status_code=204, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
        "Access-Control-Allow-Headers": "*"
    })