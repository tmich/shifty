from shifty.domain.registration_repository import RegistrationRepositoryInterface
from shifty.domain.entities import Organization, User
from sqlalchemy.exc import IntegrityError
import random
from passlib.context import CryptContext
from shifty.domain.repositories import UserRepositoryInterface

class RegistrationService:
    def __init__(self, repository: RegistrationRepositoryInterface, 
                 user_repository: UserRepositoryInterface):
        self.repository = repository
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _generate_unique_org_code(self):
        while True:
            code = f"{random.randint(100000, 999999)}"
            if not self.repository.get_organization_by_code(code):
                return code

    def register_organization(self, org_name, user_email, user_password, full_name):
        org_code = self._generate_unique_org_code()
        password_hash = self.pwd_context.hash(user_password)
        try:
            org = Organization(name=org_name, org_code=org_code)
            org = self.repository.add_organization(org)
            user = User(
                full_name=full_name,
                email=user_email,
                role="manager",
                is_active=True,
                organization_id=org.id
            )
            self.user_repository.add(user)
            return org_code
        except IntegrityError:
            raise ValueError("Email already exists in this organization")

    def join_organization(self, org_code, user_email, user_password, full_name):
        password_hash = self.pwd_context.hash(user_password)
        org = self.repository.get_organization_by_code(org_code)
        if not org:
            raise ValueError("Organization not found")
        # existing = self.repository.get_user_by_email_and_org(user_email, org.id)
        existing = self.repository.get_user_by_email(user_email)
        if existing:
            raise ValueError("Email already exists in this organization")
        user = User(
            full_name=full_name,
            email=user_email,
            role="worker",
            is_active=True,
            organization_id=org.id
        )
        self.user_repository.add(user)
        return user