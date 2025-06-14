from shifty.domain.repositories import AvailabilityRepositoryInterface
from shifty.domain.entities import Availability #, AvailabilitySlot

class AvailabilityRepository(AvailabilityRepositoryInterface):
    def __init__(self, session):
        self.session = session

    def add(self, availability: Availability) -> Availability:
        """
        Add a new Availability entity to the repository.
        This method is used to create a new availability record.
        """
        if not isinstance(availability, Availability):
            raise TypeError("Expected an instance of AvailabilityCreate.")
        
        self.session.add(availability)
        self.session.commit()
        self.session.refresh(availability)
        return availability

    def save(self, availability):
        self.session.add(availability)
        self.session.commit()

    def get_all(self) -> list[Availability]:
        availabilities = self.session.query(Availability).all()
        return availabilities

    # def get_availability_on_day(self, user_id, date) -> list[AvailabilitySlot]:
    #     models = self.session.query(Availability).filter(
    #         Availability.user_id == user_id,
    #         Availability.date == date
    #     ).all()
    #     return []

    def delete(self, availability_id):
        availability = self.session.query(Availability).get(availability_id)
        if availability:
            self.session.delete(availability)
            self.session.commit()
        else:
            raise ValueError(f"Availability with id {availability_id} does not exist.")

    def update(self, availability):
        existing_availability = self.session.query(Availability).get(availability.id)
        if existing_availability:
            existing_availability.user_id = availability.user_id
            existing_availability.date = availability.date
            existing_availability.start_time = availability.start_time
            existing_availability.end_time = availability.end_time
            existing_availability.note = availability.note
            self.session.commit()
        else:
            raise ValueError(f"Availability with id {availability.id} does not exist.")

    def get_by_id(self, availability_id):
        availability = self.session.query(Availability).get(availability_id)
        if availability is None:
            raise ValueError(f"Availability with id {availability_id} does not exist.")
        return availability

    def get_by_user_id(self, user_id):
        models = self.session.query(Availability).filter(
            Availability.user_id == user_id
        ).all()
        return models

    def get_by_user_id_and_date(self, user_id, date):
        models = self.session.query(Availability).filter(
            Availability.user_id == user_id,
            Availability.date == date
        ).all()
        return models
    
    def get_by_date(self, date):
        models = self.session.query(Availability).filter(
            Availability.date == date
        ).all()
        return models
