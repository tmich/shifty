from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from shifty.domain.entities import Organization, User

class RegistrationRepositoryInterface(ABC):
    @abstractmethod
    def get_organization_by_code(self, org_code: str) -> Optional[Organization]:
        pass

    @abstractmethod
    def get_organization_by_name(self, name: str) -> Optional[Organization]:
        pass

    @abstractmethod
    def add_organization(self, org: Organization) -> Organization:
        pass

    # @abstractmethod
    # def add_user(self, user: User) -> User:
    #     pass

    @abstractmethod
    def get_user_by_email_and_org(self, email: str, org_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass
