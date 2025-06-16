from datetime import date, datetime, time
from uuid import uuid4, UUID
from shifty.domain.entities import Availability
from shifty.domain.repositories import AvailabilityRepositoryInterface
from shifty.domain.exceptions import InvalidDateRangeException, NotExistsException, InvalidAvailabilityException
from shifty.application.dto.availability_dto import AvailabilityCreate, AvailabilityUpdate


def start_time_must_be_before_end_time(start_time: time, end_time: time) -> bool:
    """
    Validates that the start time is before the end time.
    :param start_time: The start time of the availability.
    :param end_time: The end time of the availability.
    """
    return start_time < end_time

def availability_date_must_be_today_or_future(date: date) -> bool:
    """
    Validates that the availability date is today or in the future.
    :param date: The date of the availability.
    """
    return date >= datetime.now().date()

def availability_must_not_overlap(existing_availabilities: list[Availability], new_availability: Availability) -> bool:
    """
    Validates that the new availability does not overlap with existing availabilities.
    :param existing_availabilities: List of existing availabilities.
    :param new_availability: The new availability to check against existing ones.
    """
    for existing in existing_availabilities:
        if (existing.date == new_availability.date and
            existing.start_time < new_availability.end_time and
            existing.end_time > new_availability.start_time):
            return False
    return True

class AvailabilityService:
    def __init__(self, repository: AvailabilityRepositoryInterface):
        self.repository = repository

    def create(self, data: AvailabilityCreate) -> Availability:
        # Validate the start and end times
        if not start_time_must_be_before_end_time(data.start_time, data.end_time):
            raise InvalidDateRangeException("Start time must be before end time.")
        
        # Validate the availability date
        if not availability_date_must_be_today_or_future(data.date):
            raise InvalidDateRangeException("Availability date must be today or in the future.")
        
        # Retrieve existing availabilities for the user on the same date
        existing_availabilities = self.repository.get_by_user_id_and_date(data.user_id, data.date)
        # Validate that the new availability does not overlap with existing ones
        new_availability = Availability(
            id=uuid4(),  # Assuming the ID is generated elsewhere or by the database
            user_id=data.user_id,
            organization_id=data.organization_id,  # Assuming this is part of the DTO
            date=data.date,
            start_time=data.start_time,
            end_time=data.end_time,
            created_at=datetime.now(),
            note=data.note,  # Assuming note is optional and can be None
        )

        if not availability_must_not_overlap(existing_availabilities, new_availability):
            raise InvalidAvailabilityException("New availability overlaps with existing availabilities.")

        entity = Availability(
            id=uuid4(),  # Assuming the ID is generated elsewhere or by the database
            user_id=data.user_id,
            organization_id=data.organization_id,  # Assuming this is part of the DTO
            date=data.date,
            start_time=data.start_time,
            end_time=data.end_time,
            created_at=datetime.now(),
            note=data.note,  # Assuming note is optional and can be None
        )
        saved = self.repository.add(entity)
        return saved

    def list_all(self) -> list[Availability]:
        results = self.repository.get_all()
        return results
        #return [AvailabilityRead(id=uuid4(), user_id=uuid4(), date=datetime.now().date(), start_time=datetime.now().time(), end_time=datetime.now().time(), created_at=datetime.now()),]  # Placeholder for actual implementation

    def delete(self, availability_id: UUID) -> None:
        """
        Deletes an availability with the given ID.
        
        Args:
            availability_id: UUID of the availability to delete
            
        Raises:
            NotExistsException: If the availability does not exist
        """
        try:
            self.repository.delete(availability_id)
        except ValueError as ex:
            raise NotExistsException(f"Availability with ID {availability_id} does not exist") from ex

    def update(self, id: UUID, availability: AvailabilityUpdate) -> None:
        self.repository.update(id, availability)

    def get_by_id(self, availability_id: UUID) -> Availability:
        try:
            return self.repository.get_by_id(availability_id)
        except ValueError:
            raise NotExistsException(f"availability with id {availability_id} does not exist")
        
    def get_by_user_id(self, user_id: UUID) -> list[Availability]:
        """
        Retrieves all availabilities for a specific user.
        :param user_id: The ID of the user.
        :return: A list of Availability entities for the user.
        """
        return self.repository.get_by_user_id(user_id)

    def get_by_user_id_and_date(self, user_id: UUID, date: date) -> list[Availability]:
        """
        Retrieves all availabilities for a specific user on a specific date.
        :param user_id: The ID of the user.
        :param date: The date to filter availabilities.
        :return: A list of Availability entities for the user on the specified date.
        """
        return self.repository.get_by_user_id_and_date(user_id, date)
    
    def get_by_date(self, date: date) -> list[Availability]:
        """
        Retrieves all availabilities for a specific date.
        :param date: The date to filter availabilities.
        :return: A list of Availability entities for the specified date.
        """
        return self.repository.get_by_date(date)