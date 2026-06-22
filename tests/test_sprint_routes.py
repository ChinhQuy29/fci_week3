import requests
import os
from dotenv import load_dotenv

load_dotenv()

SPRINT_ENDPOINT = os.getenv("SPRINT_ENDPOINT")

def test_can_list_sprints():
    response = requests.get(SPRINT_ENDPOINT)
    assert response.status_code == 200

def test_can_get_sprint():
    sprint_id = 1
    response = requests.get(f"{SPRINT_ENDPOINT}/{sprint_id}")
    assert response.status_code == 200

    data = response.json()
    print(data)

def test_sprint_not_found():
    sprint_id = 3
    response = requests.get(f"{SPRINT_ENDPOINT}/{sprint_id}")
    assert response.status_code == 404

    print(response.json())

def test_can_create_sprint():
    payload = {
        "title": "Sprint 3",
        "from_date": "2026-07-31",
        "to_date": "2026-08-14"
    }
    
    header = {
        "x-actor-id": "1"
    }
    
    response = requests.post(SPRINT_ENDPOINT, json=payload, headers=header)
    assert response.status_code == 201

    data = response.json()
    print(data)

def test_permission_error_on_create_sprint():
    payload = {
        "title": "Sprint 4",
        "from_date": "2026-08-15",
        "to_date": "2026-08-29"
    }
    
    header = {
        "x-actor-id": "2"  # Assuming user with ID 2 does not have permission
    }
    
    response = requests.post(SPRINT_ENDPOINT, json=payload, headers=header)
    assert response.status_code == 403

    print(response.json())

def test_value_error_on_create_sprint():
    payload = {
        "title": "Sprint 5",
        "from_date": "2026-09-01",
        "to_date": "2026-08-31"  # Invalid date range
    }
    
    header = {
        "x-actor-id": "1"
    }
    
    response = requests.post(SPRINT_ENDPOINT, json=payload, headers=header)
    assert response.status_code == 400

    print(response.json())

def test_can_add_member():
    sprint_id = 1
    payload = {
        "user_id": 2
    }
    
    header = {
        "x-actor-id": "1"
    }
    
    response = requests.post(f"{SPRINT_ENDPOINT}/{sprint_id}", json=payload, headers=header)
    assert response.status_code == 200

    data = response.json()
    print(data)

def test_permission_error_on_add_member():
    sprint_id = 1
    payload = {
        "user_id": 3
    }
    
    header = {
        "x-actor-id": "2"  # Assuming user with ID 2 does not have permission
    }
    
    response = requests.post(f"{SPRINT_ENDPOINT}/{sprint_id}", json=payload, headers=header)
    assert response.status_code == 403

    print(response.json())

def test_value_error_on_add_member():
    sprint_id = 1
    payload = {
        "user_id": 999  # Assuming user with ID 999 does not exist
    }
    
    header = {
        "x-actor-id": "1"
    }
    
    response = requests.post(f"{SPRINT_ENDPOINT}/{sprint_id}", json=payload, headers=header)
    assert response.status_code == 400

    print(response.json())

def test_can_activate_sprint():
    sprint_id = 1
    
    header = {
        "x-actor-id": "1"
    }
    
    response = requests.put(f"{SPRINT_ENDPOINT}/{sprint_id}/activate", headers=header)
    assert response.status_code == 200

    data = response.json()
    print(data)

def test_permission_error_on_activate_sprint():
    sprint_id = 1
    
    header = {
        "x-actor-id": "2"  # Assuming user with ID 2 does not have permission
    }
    
    response = requests.put(f"{SPRINT_ENDPOINT}/{sprint_id}/activate", headers=header)
    assert response.status_code == 403

    print(response.json())

def test_value_error_on_activate_sprint():
    sprint_id = 999  # Assuming sprint with ID 999 does not exist
    
    header = {
        "x-actor-id": "1"
    }
    
    response = requests.put(f"{SPRINT_ENDPOINT}/{sprint_id}/activate", headers=header)
    assert response.status_code == 400

    print(response.json())

def test_can_close_sprint():
    sprint_id = 1
    
    header = {
        "x-actor-id": "1"
    }
    
    response = requests.put(f"{SPRINT_ENDPOINT}/{sprint_id}/close", headers=header)
    assert response.status_code == 200

    data = response.json()
    print(data)

def test_permission_error_on_close_sprint():
    sprint_id = 1
    
    header = {
        "x-actor-id": "2"  # Assuming user with ID 2 does not have permission
    }
    
    response = requests.put(f"{SPRINT_ENDPOINT}/{sprint_id}/close", headers=header)
    assert response.status_code == 403

    print(response.json())

def test_value_error_on_close_sprint():
    sprint_id = 999  # Assuming sprint with ID 999 does not exist
    
    header = {
        "x-actor-id": "1"
    }
    
    response = requests.put(f"{SPRINT_ENDPOINT}/{sprint_id}/close", headers=header)
    assert response.status_code == 400

    print(response.json())

