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
