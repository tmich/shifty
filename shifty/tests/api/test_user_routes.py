import os
import uuid

def test_list_users_and_delete(client):
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
