import os
import uuid
from fastapi.testclient import TestClient
from shifty.main import app
from shifty.domain.entities import User
from sqlmodel import SQLModel, Session, create_engine
import pytest

from shifty.security.dependencies import get_current_user_id

client = TestClient(app)

app.dependency_overrides[get_current_user_id] = lambda: os.getenv("TEST_USER_ID", str(uuid.uuid4())) 

# Fixtures for test DB setup/teardown could be added here if needed

def test_create_and_get_user():
    user_data = {
        "full_name": "Test User",
        "email": "testuser@example.com",
        "role": "worker",
        "is_active": True,
        "organization_id": os.getenv('TEST_ORGANIZATION_ID', uuid.uuid4()),  # Assuming organization_id is required
    }

    # Create user
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    user = response.json()
    assert user["full_name"] == user_data["full_name"]
    assert user["email"] == user_data["email"]
    assert user["role"] == user_data["role"]
    user_id = user["id"]

    # Get user by id
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    user2 = response.json()
    assert user2["id"] == user_id


def test_list_users_and_delete():
    # List users
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    if users:
        user_id = users[0]["id"]
        # Delete user
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 204

def test_get_users_by_role():
    # Create two users with different roles
    user1 = {"full_name": "Role Worker", "email": "roleworker@example.com", "role": "worker", "is_active": True}
    user2 = {"full_name": "Role Admin", "email": "roleadmin@example.com", "role": "admin", "is_active": True}
    client.post("/users/", json=user1)
    client.post("/users/", json=user2)
    # Get users by role
    response = client.get("/users/role/worker")
    assert response.status_code == 200
    workers = response.json()
    assert any(u["role"] == "worker" for u in workers)
    response = client.get("/users/role/admin")
    assert response.status_code == 200
    admins = response.json()
    assert any(u["role"] == "admin" for u in admins)
