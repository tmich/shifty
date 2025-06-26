# shifty/domain/repositories.py
from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from uuid import UUID
from datetime import date
from shifty.application.dto.availability_dto import AvailabilityUpdate
from shifty.domain.entities import Availability, User, Shift, ShiftSlot

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

# Repository interface for managing User entities
class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Retrieve a User entity by its ID.
        :param user_id: UUID of the user to be retrieved.
        :return: User entity corresponding to the provided ID, or None if not found.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        """
        Retrieve all User entities from the repository.
        This method is used to fetch all user records.
        """
        pass

    @abstractmethod
    def add(self, user: User) -> User:
        """
        Add a new User entity to the repository.
        This method is used to create a new user record.
        """
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        """
        Delete a User entity by its ID.
        :param user_id: UUID of the user to be deleted.
        """
        pass

    @abstractmethod
    def get_by_role(self, role: str) -> List[User]:
        """
        Get all User entities with a specific role.
        :param role: Role of the users to be queried.
        :return: List of User entities with the specified role.
        """
        pass


class ShiftRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, shift_id: UUID) -> Optional[Shift]:
        """
        Retrieve a Shift entity by its ID.
        :param shift_id: UUID of the shift to be retrieved.
        :return: Shift entity corresponding to the provided ID, or None if not found.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Shift]:
        """
        Retrieve all Shift entities from the repository.
        This method is used to fetch all shift records.
        """
        pass

    @abstractmethod
    def add(self, shift: Shift) -> Shift:
        """
        Add a new Shift entity to the repository.
        This method is used to create a new shift record.
        """
        pass

    @abstractmethod
    def delete(self, shift_id: UUID) -> None:
        """
        Delete a Shift entity by its ID.
        :param shift_id: UUID of the shift to be deleted.
        """
        pass

    @abstractmethod
    def get_by_date(self, date: date) -> List[Shift]:
        """
        Get all Shift entities for a specific date.
        :param date: Date for which shifts are being queried.
        :return: List of Shift entities for the specified date.
        """
        pass

    @abstractmethod
    def get_shift_slots(self) -> List[ShiftSlot]:
        """
        Retrieve all ShiftSlot entities from the repository.
        This method is used to fetch all shift slot records.
        """
        pass
    
    @abstractmethod
    def get_shift_slots_by_organization(self, organization_id: UUID) -> List[ShiftSlot]:
        """
        Get all ShiftSlot entities for a specific organization.
        :param organization_id: UUID of the organization whose shift slots are being queried.
        :return: List of ShiftSlot entities for the specified organization.
        """
        pass
    
    @abstractmethod
    def add_shift_slot(self, shift_slot: ShiftSlot) -> ShiftSlot:
        """
        Add a new ShiftSlot entity to the repository.
        This method is used to create a new shift slot record.
        """
        pass
    
    @abstractmethod
    def update_shift_slot(self, shift_slot_id: UUID, data: dict) -> ShiftSlot:
        """
        Update an existing ShiftSlot entity.
        :param shift_slot_id: UUID of the shift slot to be updated.
        :param data: Dictionary containing the fields to be updated.
        :return: Updated ShiftSlot entity.
        """
        pass
    
    @abstractmethod
    def delete_shift_slot(self, shift_slot_id: UUID) -> None:
        """
        Delete a ShiftSlot entity by its ID.
        :param shift_slot_id: UUID of the shift slot to be deleted.
        """
        pass
    
    @abstractmethod
    def get_shift_slot_by_id(self, shift_slot_id: UUID) -> Optional[ShiftSlot]:
        """
        Retrieve a ShiftSlot entity by its ID.
        :param shift_slot_id: UUID of the shift slot to be retrieved.
        :return: ShiftSlot entity corresponding to the provided ID, or None if not found.
        """
        pass

    @abstractmethod
    def get_by_user(self, user_id: UUID) -> List[Shift]:
        """
        Get all shifts for a specific user.
        :param user_id: UUID of the user whose shifts are being queried.
        :return: List of Shift entities for the specified user.
        """
        pass

    @abstractmethod
    def get_by_user_and_date(self, user_id: UUID, date: date) -> List[Shift]:
        """
        Get all shifts for a specific user on a specific date.
        :param user_id: UUID of the user whose shifts are being queried.
        :param date: Date for which shifts are being queried.
        :return: List of Shift entities for the specified user and date.
        """
        pass

    @abstractmethod
    def update(self, shift_id: UUID, data: dict) -> Shift:
        """
        Update an existing Shift entity.
        :param shift_id: UUID of the shift to be updated.
        :param data: Dictionary containing the fields to be updated.
        :return: Updated Shift entity.
        """
        pass
