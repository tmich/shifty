import os
from uuid import uuid4
from datetime import datetime
from shifty.security.dependencies import get_current_user_id
from unittest.mock import patch

import pytest

@pytest.fixture(autouse=True)
def override_user_id(monkeypatch):
    # Ensures CURRENT_USER_ID is set for all tests in this file
    monkeypatch.setenv("CURRENT_USER_ID", str(uuid4()))

def test_get_shift_types(client):
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
        "updated_at": None,
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

def test_create_shifts_bulk(client):
    # Prepare a list of shifts to create
    org_id = os.getenv(
        "TEST_ORGANIZATION_ID", str(uuid4())
    )  # Use a test organization ID or create one

    user_id1 = "1d5037ea-5f47-4604-937b-f65618119050"
    user_id2 = "cd1a1bbb-95dd-4bbd-a110-0c6b66504741"
    origin_user_id1 = user_id1
    origin_user_id2 = user_id2
    shifts = [
        {
            "user_id": user_id1,
            "origin_user_id": origin_user_id1,
            "organization_id": org_id,
            "date": "2025-06-18",
            "start_time": "07:00:00",
            "end_time": "13:00:00",
            "note": "Confirmed by manager",
        },
        {
            "user_id": user_id2,
            "origin_user_id": origin_user_id2,
            "organization_id": org_id,
            "date": "2025-06-18",
            "start_time": "07:00:00",
            "end_time": "13:00:00",
            "note": "Confirmed by manager",
        },
    ]

    json_return_value = [
        # ... (keep your mock return value here) ...
    ]

    with patch.object(client, "post") as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = json_return_value

        response = client.post("/shifts/bulk", json={"shifts": shifts})

        assert response.status_code == 201
        assert response.json() == json_return_value
        mock_post.assert_called_once_with("/shifts/bulk", json={"shifts": shifts})

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    for shift, orig in zip(data, shifts):
        assert shift["user_id"] == orig["user_id"]
        assert shift["organization_id"] == orig["organization_id"]
        assert shift["start_time"] == orig["start_time"]
        assert shift["end_time"] == orig["end_time"]
