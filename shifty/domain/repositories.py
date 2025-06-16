# shifty/domain/repositories.py
from abc import ABC, abstractmethod
from datetime import date
from typing import List
from uuid import UUID
from shifty.application.dto.availability_dto import AvailabilityUpdate
from shifty.domain.entities import Availability #, AvailabilitySlot

# Repository interface for managing Availability entities
class AvailabilityRepositoryInterface(ABC):
    @abstractmethod
    def add(self, availability: Availability) -> Availability:
        """
        Add a new Availability entity to the repository.
        This method is used to create a new availability record.
        """
        pass

    @abstractmethod
    def update(self, id: UUID, availability: AvailabilityUpdate) -> Availability:
        """
        Update an existing Availability entity.
        :param availability: Availability entity with updated information.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Availability]:
        """
        Retrieve all Availability entities from the repository.
        This method is used to fetch all availability records.
        """
        pass

    # @abstractmethod
    # def get_availability_on_day(self, user_id: UUID, date: date) -> list[AvailabilitySlot]:
    #     """
    #     Get all availability slots for a specific user on a given date.
    #     :param user_id: UUID of the user whose availability is being queried.
    #     :param date: Date for which availability is being queried.
    #     :return: List of AvailabilitySlot entities for the specified user and date.
    #     """
    #     pass

    @abstractmethod
    def delete(self, availability_id: UUID) -> None:
        """
        Delete an Availability entity by its ID.
        :param availability_id: UUID of the availability to be deleted.
        """
        pass

    @abstractmethod
    def get_by_id(self, availability_id: UUID) -> Availability:
        """
        Retrieve an Availability entity by its ID.
        :param availability_id: UUID of the availability to be retrieved.
        :return: Availability entity corresponding to the provided ID.
        """
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: UUID) -> List[Availability]:
        """
        Get all Availability entities for a specific user.
        :param user_id: UUID of the user whose availability is being queried.
        :return: List of Availability entities for the specified user.
        """
        pass

    @abstractmethod
    def get_by_date(self, date: date) -> List[Availability]:
        """
        Get all Availability entities for a specific date.
        :param date: Date for which availability is being queried.
        :return: List of Availability entities for the specified date.
        """
        pass

    @abstractmethod
    def get_by_user_id_and_date(self, user_id: UUID, date: date) -> List[Availability]:
        """
        Get all Availability entities for a specific user on a specific date.
        :param user_id: UUID of the user whose availability is being queried.
        :param date: Date for which availability is being queried.
        :return: List of Availability entities for the specified user and date.
        """
        pass
