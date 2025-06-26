from shifty.domain.registration_repository import RegistrationRepositoryInterface
from shifty.domain.entities import Organization, User, ShiftSlot
from sqlalchemy.exc import IntegrityError
import random
from passlib.context import CryptContext
from shifty.domain.repositories import UserRepositoryInterface, ShiftRepositoryInterface
from datetime import datetime, time

class RegistrationService:
    def __init__(self, repository: RegistrationRepositoryInterface, 
                 user_repository: UserRepositoryInterface,
                 shift_repository: ShiftRepositoryInterface):
        self.repository = repository
        self.user_repository = user_repository
        self.shift_repository = shift_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _generate_unique_org_code(self):
        while True:
            code = f"{random.randint(100000, 999999)}"
            if not self.repository.get_organization_by_code(code):
                return code

    def _create_default_shift_slots(self, organization_id):
        """Create default shift slots for a new organization"""
        default_slots = [
            {
                "name": "Mattina/Morning",
                "start_time": time(6, 0),
                "end_time": time(13, 0),
                "description": "Turno mattutino - Morning shift"
            },
            {
                "name": "Pomeriggio/Afternoon", 
                "start_time": time(13, 0),
                "end_time": time(18, 0),
                "description": "Turno pomeridiano - Afternoon shift"
            },
            {
                "name": "Chiusura/Closing time",
                "start_time": time(18, 0),
                "end_time": time(22, 0),
                "description": "Turno serale - Evening/closing shift"
            }
        ]
        
        for slot_data in default_slots:
            shift_slot = ShiftSlot(
                organization_id=organization_id,
                name=slot_data["name"],
                start_time=slot_data["start_time"],
                end_time=slot_data["end_time"],
                description=slot_data["description"],
                expected_workers=1,
                is_active=True,
                created_at=datetime.now()
            )
            self.shift_repository.add_shift_slot(shift_slot)

    def register_organization(self, org_name, user_email, user_password, full_name):
        org_code = self._generate_unique_org_code()
        password_hash = self.pwd_context.hash(user_password)
        try:
            org = Organization(name=org_name, org_code=org_code)
            org = self.repository.add_organization(org)
            
            # Create default shift slots for the new organization
            self._create_default_shift_slots(org.id)
            
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