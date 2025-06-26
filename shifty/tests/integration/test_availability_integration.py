import pytest
from uuid import uuid4
from datetime import date, timedelta

def test_create_and_delete_availability(client):
    """Test creating an availability and then deleting it"""
    user_id = uuid4()
    org_id = uuid4()
    
    # First create an availability
    tomorrow = date.today() + timedelta(days=1)
    availability_data = {
        "user_id": str(user_id),
        "organization_id": str(org_id),
        "date": tomorrow.isoformat(),
        "start_time": "09:00:00",
        "end_time": "17:00:00",
        "note": "Test availability"
    }
    
    # Create the availability
    response = client.post("/availabilities/", json=availability_data)
    assert response.status_code == 201
    result = response.json()
    assert result["result"] == "success"
    availability_id = result["availability"]["id"]
    
    # Verify it exists
    response = client.get(f"/availabilities/{availability_id}")
    assert response.status_code == 200
    
    # Delete the availability
    response = client.delete(f"/availabilities/{availability_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    response = client.get(f"/availabilities/{availability_id}")
    assert response.status_code == 404
