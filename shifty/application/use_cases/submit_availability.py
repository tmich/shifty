from datetime import datetime
from typing import Optional
from uuid import UUID
from shifty.application.services import UseCase
from shifty.application.dto.availability_dto import AvailabilityCreate
from shifty.domain.entities import Availability
from shifty.domain.repositories import AvailabilityRepositoryInterface


class SubmitAvailabilityUseCase(UseCase):
    """
    Use case for registering availability.
    This use case handles the logic for submitting availability data.
    """

    def __init__(self, availability_repository: AvailabilityRepositoryInterface):
        self.availability_repository = availability_repository

    def execute(self, input_dto: AvailabilityCreate):
        """
        Executes the use case with the provided input DTO.
        
        :param input_dto: Data Transfer Object containing the availability data.
        :return: Confirmation of successful registration.
        """
        # Here you would typically validate the input_dto and convert it to a domain entity
        # For example:
        # availability = Availability(**input_dto.__dict__)
        
        
        # Save the availability using the repository
        availability = Availability(
            id=UUID(),  # Assuming the ID is generated elsewhere or by the database
            user_id=input_dto.user_id,
            date=input_dto.date,
            start_time=input_dto.start_time,
            end_time=input_dto.end_time,
            created_at=datetime.now(),
        )

        self.availability_repository.add(availability)
        
        return {"status": "success", "message": "Availability registered successfully."}

# Note: The input_dto should be an instance of a DTO class that matches the expected structure
# for the availability data, such as AvailabilityRequest.

