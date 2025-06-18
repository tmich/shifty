from sqlmodel import Session, select
from typing import Optional
from uuid import UUID
from shifty.domain.entities import Organization, User
from shifty.domain.registration_repository import RegistrationRepositoryInterface

class RegistrationRepository(RegistrationRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def get_organization_by_code(self, org_code: str) -> Optional[Organization]:
        return self.session.exec(select(Organization).where(Organization.org_code == org_code)).first()

    def get_organization_by_name(self, name: str) -> Optional[Organization]:
        return self.session.exec(select(Organization).where(Organization.name == name)).first()

    def add_organization(self, org: Organization) -> Organization:
        self.session.add(org)
        self.session.commit()
        self.session.refresh(org)
        return org

    # def add_user(self, user: User) -> User:
    #     self.session.add(user)
    #     self.session.commit()
    #     self.session.refresh(user)
    #     return user

    def get_user_by_email_and_org(self, email: str, org_id: UUID) -> Optional[User]:
        return self.session.exec(select(User).where(User.email == email, User.organization_id == org_id)).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.session.exec(select(User).where(User.email == email)).first()
