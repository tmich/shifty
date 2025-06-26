import pytest
from uuid import uuid4

def test_signup_and_login(client):
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

def test_refresh_token_flow(client):
    email = f"user{uuid4()}@test.com"
    password = "testpassword123"
    # Signup
    resp = client.post("/auth/signup", json={"username": email, "password": password})
    assert resp.status_code == 201
    data = resp.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    assert access_token
    assert refresh_token

    # Login to get new tokens
    resp2 = client.post("/auth/login", json={"username": email, "password": password})
    assert resp2.status_code == 200
    data2 = resp2.json()
    access_token2 = data2["access_token"]
    refresh_token2 = data2["refresh_token"]
    assert access_token2
    assert refresh_token2
    assert refresh_token2 != refresh_token  # Should rotate on login

    # Use refresh endpoint to get new tokens
    resp3 = client.post("/auth/refresh", json={"username": email, "refresh_token": refresh_token2})
    assert resp3.status_code == 200
    data3 = resp3.json()
    access_token3 = data3["access_token"]
    refresh_token3 = data3["refresh_token"]
    assert access_token3
    assert refresh_token3
    assert refresh_token3 != refresh_token2  # Should rotate on refresh

    # Using an invalid refresh token should fail
    resp4 = client.post("/auth/refresh", json={"username": email, "refresh_token": "invalidtoken"})
    assert resp4.status_code == 401

    # Using an old (already rotated) refresh token should fail
    resp5 = client.post("/auth/refresh", json={"username": email, "refresh_token": refresh_token2})
    assert resp5.status_code == 401
