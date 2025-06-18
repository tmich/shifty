import pytest
from fastapi.testclient import TestClient
from shifty.main import app
from uuid import uuid4

client = TestClient(app)

def test_signup_and_login():
    email = f"user{uuid4()}@test.com"
    password = "testpassword123"
    # Signup
    resp = client.post("/auth/signup", json={"username": email, "password": password})
    assert resp.status_code == 201
    token = resp.json()["access_token"]
    assert token
    # Login
    resp2 = client.post("/auth/login", json={"username": email, "password": password})
    assert resp2.status_code == 200
    token2 = resp2.json()["access_token"]
    assert token2
    assert token != ""
    # Invalid login
    resp3 = client.post("/auth/login", json={"username": email, "password": "wrongpass"})
    assert resp3.status_code == 401
