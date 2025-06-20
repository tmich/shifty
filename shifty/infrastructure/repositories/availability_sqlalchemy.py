from uuid import UUID
from shifty.application.dto.availability_dto import AvailabilityUpdate
from shifty.domain.repositories import AvailabilityRepositoryInterface
from shifty.domain.entities import Availability #, AvailabilitySlot
from sqlmodel import Session, select  # Assuming SQLModel is used for ORM

class AvailabilityRepository(AvailabilityRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def add(self, availability: Availability) -> Availability:
        """
        Add a new Availability entity to the repository.
        This method is used to create a new availability record.
        """
        if not isinstance(availability, Availability):
            raise TypeError("Expected an instance of Availability.")
        
        self.session.add(availability)
        self.session.commit()
        self.session.refresh(availability)
        return availability

    def save(self, availability):
        self.session.add(availability)
        self.session.commit()

    def get_all(self) -> list[Availability]:
        stmt = select(Availability)
        availabilities = list(self.session.exec(stmt).all())
        return availabilities

    # def get_availability_on_day(self, user_id, date) -> list[AvailabilitySlot]:
    #     models = self.session.query(Availability).filter(
    #         Availability.user_id == user_id,
    #         Availability.date == date
    #     ).all()
    #     return []

    def delete(self, availability_id):
        availability = self.session.get(Availability, availability_id)
        if availability:
            self.session.delete(availability)
            self.session.commit()
        else:
            raise ValueError(f"Availability with id {availability_id} does not exist.")
    
    def update(self, id: UUID, availability: AvailabilityUpdate) -> Availability:
        #existing_availability = self.session.get(Availability, id)
        select1 = select(Availability).where(Availability.id == id)
        existing_availability = self.session.exec(select1).first()

        if not existing_availability:
            raise ValueError(f"Availability with id {id} does not exist.")
        
        #availability_data = availability.model_dump(exclude_unset=True)
        #existing_availability.sqlmodel_update(availability_data)
        existing_availability.note = availability.note
        
        self.session.add(existing_availability)
        self.session.commit()
        self.session.refresh(existing_availability)
        return existing_availability
        

    def get_by_id(self, availability_id):
        availability = self.session.get(Availability, availability_id)
        if availability is None:
            raise ValueError(f"Availability with id {availability_id} does not exist.")
        return availability

    def get_by_user_id(self, user_id):
        qry = select(Availability).where(Availability.user_id == user_id)
        return list(self.session.exec(qry).all())
    
    def get_by_user_id_and_date(self, user_id, date):
        qry = select(Availability).where(
            Availability.user_id == user_id).where(Availability.date == date)
        return list(self.session.exec(qry).all())
    
    def get_by_date(self, date):
        qry = select(Availability).where(Availability.date == date)
        return list(self.session.exec(qry).all())
