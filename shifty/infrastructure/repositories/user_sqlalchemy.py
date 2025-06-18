from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from shifty.domain.entities import User
from shifty.domain.repositories import UserRepositoryInterface

class UserRepository(UserRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        return self.session.get(User, user_id)

    def get_all(self) -> List[User]:
        return list(self.session.exec(select(User)).all())

    def add(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user_id: UUID) -> None:
        user = self.session.get(User, user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
        else:
            raise ValueError("User not found")
        
    def get_by_role(self, role: str) -> List[User]:
        return list(self.session.exec(select(User).where(User.role == role)).all())
