import pytest
from sqlmodel import Session, create_engine, SQLModel
from shifty.domain.entities import Organization, User
from shifty.infrastructure.repositories.registration_sqlalchemy import RegistrationRepository
from shifty.infrastructure.repositories.user_sqlalchemy import UserRepository

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def repo(session):
    return RegistrationRepository(session)

@pytest.fixture
def user_repo(session):
    return UserRepository(session)

def test_add_and_get_organization(repo):
    org = Organization(name="TestOrg", org_code="123456")
    repo.add_organization(org)
    found = repo.get_organization_by_code("123456")
    assert found is not None
    assert found.name == "TestOrg"

def test_add_and_get_user(repo, user_repo: UserRepository):
    org = Organization(name="TestOrg2", org_code="654321")
    repo.add_organization(org)
    user = User(full_name="Test User", email="test@example.com", role="worker", is_active=True, organization_id=org.id)
    user_repo.add(user)
    found = repo.get_user_by_email_and_org("test@example.com", org.id)
    assert found is not None
    assert found.full_name == "Test User"
