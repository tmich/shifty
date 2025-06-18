from shifty.domain.repositories import UserRepositoryInterface
from shifty.domain.entities import User
from typing import List, Optional
from uuid import UUID

class UserService:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        return self.repository.get_by_id(user_id)

    def get_all(self) -> List[User]:
        return self.repository.get_all()

    def add(self, user: User) -> User:
        return self.repository.add(user)

    def delete(self, user_id: UUID) -> None:
        self.repository.delete(user_id)

    def get_by_role(self, role: str) -> List[User]:
        return self.repository.get_by_role(role)
