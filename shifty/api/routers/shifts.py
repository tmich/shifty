from uuid import UUID
from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from shifty.dependencies import get_shift_service
from shifty.domain.entities import Shift, ShiftRead, ShiftType
from shifty.application.dto.shift_dto import ShiftCreate, ShiftCalculationRequest, ShiftCalculationResult, ShiftBulkCreate
from shifty.application.use_cases.shift_service import ShiftService
from shifty.domain.exceptions import NotExistsException

router = APIRouter(prefix="/shifts", tags=["shifts"])


@router.post("/", response_model=Shift, status_code=201)
def create_shift(
    data: ShiftCreate,
    service: ShiftService = Depends(get_shift_service)
):

    try:
        # Create the shift using the service
        shift = service.create(data)
        return shift
    except Exception as e:
        # Handle exceptions, e.g., overlapping shifts
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/", response_model=List[ShiftRead])
def list_shifts(service: ShiftService = Depends(get_shift_service)):
    shifts = service.list_all()
    return shifts

@router.get("/{shift_id}", response_model=Optional[ShiftRead])
def get_shift(shift_id: UUID, service: ShiftService = Depends(get_shift_service)):
    try:
        return service.get_by_id(shift_id)
    except NotExistsException:
        raise HTTPException(status_code=404, detail="Shift not found")

@router.delete("/{shift_id}", status_code=204)
def delete_shift(shift_id: UUID, response: Response, service: ShiftService = Depends(get_shift_service)):
    try:
        service.delete(shift_id)
    except NotExistsException:
        raise HTTPException(status_code=404, detail="Shift not found")

@router.get("/date/{date}", response_model=List[ShiftRead])
def get_shifts_by_date(date: date, service: ShiftService = Depends(get_shift_service)):
    shifts = service.get_by_date(date)
    if not shifts:
        raise HTTPException(status_code=404, detail="No shifts found for this date")
    return shifts

@router.get("/user/{user_id}", response_model=List[ShiftRead])
def get_shifts_by_user(user_id: UUID, service: ShiftService = Depends(get_shift_service)):
    shifts = service.get_by_user(user_id)
    if not shifts:
        raise HTTPException(status_code=404, detail="No shifts found for this user")
    return shifts

@router.get("/user/{user_id}/date/{date}", response_model=List[ShiftRead])
def get_shifts_by_user_and_date(user_id: UUID, date: date, service: ShiftService = Depends(get_shift_service)):
    shifts = service.get_by_user_and_date(user_id, date)
    if not shifts:
        raise HTTPException(status_code=404, detail="No shifts found for this user on this date")
    return shifts

@router.put("/{shift_id}", response_model=ShiftRead)
def update_shift(
    shift_id: UUID,
    data: ShiftCreate,
    service: ShiftService = Depends(get_shift_service)
):
    try:
        updated = service.update(shift_id, data.dict(exclude_unset=True))
        return updated
    except NotExistsException:
        raise HTTPException(status_code=404, detail="Shift not found")

@router.get("/types/all", response_model=List[ShiftType])
def get_shift_types(service: ShiftService = Depends(get_shift_service)):
    return service.get_shift_types()

@router.options("/")
def options_shifts():
    return Response(status_code=204, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
        "Access-Control-Allow-Headers": "*"
    })

@router.post("/calculate", response_model=List[ShiftCalculationResult])
def calculate_shifts(
    request: ShiftCalculationRequest,
    service: ShiftService = Depends(get_shift_service)
):
    return service.calculate_shifts(request)

@router.post("/bulk", response_model=List[Shift], status_code=201)
def create_shifts_bulk(
    data: ShiftBulkCreate,
    service: ShiftService = Depends(get_shift_service)
):
    try:
        shifts = service.create_bulk(data.shifts)
        return shifts
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))