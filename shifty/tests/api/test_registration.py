import pytest
from fastapi.testclient import TestClient
from shifty.main import app

client = TestClient(app)

def test_register_organization_and_join():
    # Register new org
    resp = client.post("/register/organization", json={
        "organization_name": "TestOrg",
        "user_email": "owner@test.com",
        "user_password": "pw123"
    })
    assert resp.status_code == 200
    org_code = resp.json()["org_code"]

    # Join as worker
    resp2 = client.post("/register/join", json={
        "org_code": org_code,
        "user_email": "worker@test.com",
        "user_password": "pw456"
    })
    assert resp2.status_code == 200
    assert "access_token" in resp2.json()

    # Duplicate email in org
    resp3 = client.post("/register/join", json={
        "org_code": org_code,
        "user_email": "worker@test.com",
        "user_password": "pw789"
    })
    assert resp3.status_code == 400