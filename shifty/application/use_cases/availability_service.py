from datetime import datetime
from uuid import UUID, uuid4
from shifty.domain.entities import Availability
from shifty.domain.repositories import AvailabilityRepositoryInterface
from shifty.application.dto.availability_dto import AvailabilityCreate, AvailabilityRead


class AvailabilityService:
    def __init__(self, repository: AvailabilityRepositoryInterface):
        self.repository = repository

    def create(self, data: AvailabilityCreate) -> AvailabilityRead:
        entity = Availability(
            id=UUID(),  # Assuming the ID is generated elsewhere or by the database
            user_id=data.user_id,
            date=data.date,
            start_time=data.start_time,
            end_time=data.end_time,
            created_at=datetime.now(),
        )
        saved = self.repository.add(entity)
        return AvailabilityRead(**saved.__dict__)

    def list_all(self) -> list[AvailabilityRead]:
        results = self.repository.get_all()
        return [AvailabilityRead(**a.__dict__) for a in results]
        #return [AvailabilityRead(id=uuid4(), user_id=uuid4(), date=datetime.now().date(), start_time=datetime.now().time(), end_time=datetime.now().time(), created_at=datetime.now()),]  # Placeholder for actual implementation
