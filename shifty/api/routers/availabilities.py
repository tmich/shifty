from fastapi import APIRouter, Depends
from shifty.application.dto.availability_dto import AvailabilityCreate, AvailabilityRead
from shifty.application.use_cases.availability_service import AvailabilityService
from shifty.dependencies import get_availability_service  # Updated import

router = APIRouter(prefix="/availabilities", tags=["availabilities"])

@router.post("/", response_model=AvailabilityRead, status_code=201)
def create_availability(
    data: AvailabilityCreate,
    service: AvailabilityService = Depends(get_availability_service)
):
    return service.create(data)

@router.get("/", response_model=list[AvailabilityRead])
def list_availabilities(
    service: AvailabilityService = Depends(get_availability_service)
):
    return service.list_all()
