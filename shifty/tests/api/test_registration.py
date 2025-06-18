from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from shifty.main import app

client = TestClient(app)

def test_register_organization_and_join():
    # Register new org
    rnd = str(uuid4())[6:12]
    resp = client.post("/register/organization", json={
        "organization_name": "TestOrg",
        "user_email": f"owner-{rnd}@test.com",
        "user_password": "pw123",
        "full_name": "Test Owner"
    })
    assert resp.status_code == 200
    org_code = resp.json()["org_code"]

    # Join as worker
    rnd = str(uuid4())[6:12]
    resp2 = client.post("/register/join", json={
        "org_code": org_code,
        "user_email": f"worker_{rnd}@test.com",
        "user_password": "pw456",
        "full_name": "Test Worker"
    })
    assert resp2.status_code == 200
    assert "access_token" in resp2.json()

    # Duplicate email in org
    resp3 = client.post("/register/join", json={
        "org_code": org_code,
        "user_email": "worker@test.com",
        "user_password": "pw789",
        "full_name": "Duplicate Worker"
    })
    assert resp3.status_code == 400