import os
from fastapi.testclient import TestClient
from shifty.main import app
from uuid import uuid4
from datetime import datetime
from shifty.security.dependencies import get_current_user_id

client = TestClient(app)

app.dependency_overrides[get_current_user_id] = lambda: os.getenv("TEST_USER_ID", str(uuid4())) 

def test_get_shift_types(monkeypatch):
    # Mock response data
    fake_shift_type = {
        "id": str(uuid4()),
        "organization_id": str(uuid4()),
        "name": "Morning",
        "start_time": "08:00:00",
        "end_time": "16:00:00",
        "description": "Morning shift",
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "updated_at": None
    }
    
    # Optionally, monkeypatch the service/repo if you want to isolate from DB
    # For now, just check the endpoint exists and returns 200
    response = client.get("/shifts/types/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # If DB is empty, list may be empty; otherwise, check structure
    if response.json():
        item = response.json()[0]
        assert "id" in item
        assert "name" in item
        assert "start_time" in item
        assert "end_time" in item

def test_create_shifts_bulk():
    # Prepare a list of shifts to create
    org_id = os.getenv("TEST_ORGANIZATION_ID", str(uuid4()))  # Use a test organization ID or create one

    user_id = str(uuid4())
    origin_user_id = str(uuid4())
    shifts = [
        {
            "user_id": user_id,
            "origin_user_id": origin_user_id,
            "organization_id": org_id,
            "date": "2025-06-18",
            "start_time": "08:00:00",
            "end_time": "12:00:00",
            "note": "Confirmed by manager"
        },
        {
            "user_id": str(uuid4()),
            "origin_user_id": origin_user_id,
            "organization_id": org_id,
            "date": "2025-06-18",
            "start_time": "12:00:00",
            "end_time": "16:00:00",
            "note": "Confirmed by manager"
        }
    ]
    response = client.post("/shifts/bulk", json={"shifts": shifts})
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    for shift, orig in zip(data, shifts):
        assert shift["user_id"] == orig["user_id"]
        assert shift["organization_id"] == orig["organization_id"]
        assert shift["start_time"] == orig["start_time"]
        assert shift["end_time"] == orig["end_time"]
