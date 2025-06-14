from datetime import datetime
from shifty.domain.repositories import AvailabilityRepositoryInterface
from shifty.domain.entities import Availability, AvailabilitySlot
from shifty.infrastructure.models import AvailabilityModel

def map_availability_model_to_entity(availability_model: AvailabilityModel) -> Availability:
    """
    Maps an AvailabilityModel instance to an Availability entity.
    """
    print(f"Mapping AvailabilityModel to Availability entity: {availability_model}")
    a = Availability.model_validate(availability_model)

    return a

def map_availability_entity_to_model(entity: Availability) -> AvailabilityModel:
    """
    Maps an Availability entity to an AvailabilityModel instance.
    
    :param entity: An instance of Availability.
    :return: An instance of AvailabilityModel.
    """
    return AvailabilityModel(
        id=entity.id,
        user_id=entity.user_id,
        date=entity.date,
        start_time=entity.start_time,
        end_time=entity.end_time,
        note=entity.note,
        created_at=entity.created_at
    )


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
        
        availability_model = AvailabilityModel(
            user_id = availability.user_id,
            date = availability.date,
            start_time = availability.start_time,
            end_time = availability.end_time,
            note = availability.note,
            created_at = availability.created_at
        )
        self.session.add(availability_model)
        self.session.commit()
        self.session.refresh(availability_model)
        return map_availability_model_to_entity(availability_model)

    def save(self, availability):
        self.session.add(availability)
        self.session.commit()

    def get_all(self) -> list[Availability]:
        availabilities = self.session.query(AvailabilityModel).all()
        if availabilities:
            print(f"Id: {getattr(availabilities[0], 'id')}")
            print(f"User ID: {getattr(availabilities[0], 'user_id')}")
            print(f"Date: {getattr(availabilities[0], 'date')}")
            print(f"Start Time: {getattr(availabilities[0], 'start_time')}")
            print(f"End Time: {getattr(availabilities[0], 'end_time')}")
            print(f"Note: {getattr(availabilities[0], 'note')}")
            print(f"Created At: {getattr(availabilities[0], 'created_at')}")
        return [map_availability_model_to_entity(m) for m in availabilities]

    def get_availability_on_day(self, user_id, date) -> list[AvailabilitySlot]:
        return []
        # models = self.session.query(AvailabilityModel).filter(
        #     AvailabilityModel.user_id == user_id,
        #     AvailabilityModel.date == date
        # ).all()
        # return [map_availability_model_to_entity(m) for m in models]

    def delete(self, availability_id):
        availability = self.session.query(AvailabilityModel).get(availability_id)
        if availability:
            self.session.delete(availability)
            self.session.commit()
        else:
            raise ValueError(f"Availability with id {availability_id} does not exist.")

    def update(self, availability):
        existing_availability = self.session.query(AvailabilityModel).get(availability.id)
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
        availability = self.session.query(AvailabilityModel).get(availability_id)
        if availability is None:
            raise ValueError(f"Availability with id {availability_id} does not exist.")
        entity = map_availability_model_to_entity(availability)
        if entity is None:
            raise ValueError(f"Failed to map AvailabilityModel with id {availability_id} to Availability entity.")
        return entity

    def get_by_user_id(self, user_id):
        models = self.session.query(AvailabilityModel).filter(
            AvailabilityModel.user_id == user_id
        ).all()
        return [map_availability_model_to_entity(m) for m in models]

    def get_by_user_id_and_date(self, user_id, date):
        models = self.session.query(AvailabilityModel).filter(
            AvailabilityModel.user_id == user_id,
            AvailabilityModel.date == date
        ).all()
        return [map_availability_model_to_entity(m) for m in models]
