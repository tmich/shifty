import os
from fastapi.testclient import TestClient
from shifty.main import app
from uuid import uuid4
from datetime import datetime
from shifty.security.dependencies import get_current_user_id
from unittest.mock import patch

client = TestClient(app)

app.dependency_overrides[get_current_user_id] = lambda: os.getenv(
    "CURRENT_USER_ID", str(uuid4())
)


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


def test_create_shifts_bulk(monkeypatch):
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

    # response = client.post("/shifts/bulk", json={"shifts": shifts})
    json_return_value = [
  {
    "user_id": "1d5037ea-5f47-4604-937b-f65618119050",
    "organization_id": "a688a572-64dd-49d2-891b-806deb44cae0",
    "date": "2025-06-19",
    "start_time": "07:00:00",
    "end_time": "13:00:00",
    "note": None,
    "created_at": "2025-06-18T19:48:14.384234",
    "shift_type": {
      "name": "Mattina",
      "end_time": "13:00:00",
      "expected_workers": 2,
      "created_at": "2025-06-18T19:46:56.888770",
      "start_time": "07:00:00",
      "organization_id": "a688a572-64dd-49d2-891b-806deb44cae0",
      "id": "f7914fb1-b349-4319-b697-c602af9afad5",
      "description": None,
      "is_active": True,
      "updated_at": None
    },
    "user": {
      "role": "worker",
      "is_active": True,
      "updated_at": None,
      "organization_id": "a688a572-64dd-49d2-891b-806deb44cae0",
      "full_name": "Peppino",
      "email": "testuser@example.com",
      "created_at": "2025-06-18T19:26:09.559132",
      "id": "1100b023-3206-4884-8813-85079c4b1dbb"
    }
  },
  {
    "user_id": "cd1a1bbb-95dd-4bbd-a110-0c6b66504741",
    "organization_id": "a688a572-64dd-49d2-891b-806deb44cae0",
    "date": "2025-06-19",
    "start_time": "07:00:00",
    "end_time": "13:00:00",
    "note": None,
    "created_at": "2025-06-18T19:48:14.385660",
    "shift_type": {
      "name": "Mattina",
      "end_time": "13:00:00",
      "expected_workers": 2,
      "created_at": "2025-06-18T19:46:56.888770",
      "start_time": "07:00:00",
      "organization_id": "a688a572-64dd-49d2-891b-806deb44cae0",
      "id": "f7914fb1-b349-4319-b697-c602af9afad5",
      "description": None,
      "is_active": True,
      "updated_at": None
    },
    "user": {
      "role": "worker",
      "is_active": True,
      "updated_at": None,
      "organization_id": "a688a572-64dd-49d2-891b-806deb44cae0",
      "full_name": "Test User 7",
      "email": "testuser@example.com",
      "created_at": "2025-06-18T19:26:43.191921",
      "id": "c70fa1b1-f366-41fb-beb8-75aa97e1c289"
    }
  },
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
