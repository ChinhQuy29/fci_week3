import requests
from dotenv import load_dotenv
import os

load_dotenv()

USER_ENDPOINT = os.getenv("USER_ENDPOINT")

def test_can_create_user():
    payload = {
        "name": "testuser",
        "email": "testuser@example.com"
    }

    response = requests.post(USER_ENDPOINT, json=payload)
    assert response.status_code == 201

    data = response.json()
    print(data)

def test_value_error_on_create_user():
    payload = {
        "name": "testuser",
        "email": "testuser2@example.com"
    }

    response = requests.post(USER_ENDPOINT, json=payload)
    assert response.status_code == 400

    print(response.json())

def test_can_list_users():
    response = requests.get(USER_ENDPOINT)
    assert response.status_code == 200

    data = response.json()
    print(data)

def test_can_get_user():
    user_id = 1
    response = requests.get(f"{USER_ENDPOINT}/{user_id}")
    assert response.status_code == 200

    data = response.json()
    print(data)

def test_value_error_on_get_user():
    user_id = 999
    response = requests.get(f"{USER_ENDPOINT}/{user_id}")
    assert response.status_code == 404

    print(response.json())

def test_can_update_user():
    user_id = 1
    payload = {
        "name": "updateduser"
    }

    response = requests.put(f"{USER_ENDPOINT}/{user_id}", json=payload)
    assert response.status_code == 200

    data = response.json()
    print(data)

def test_value_error_on_update_user():
    user_id = 999
    payload = {
        "name": "updateduser"
    }

    response = requests.put(f"{USER_ENDPOINT}/{user_id}", json=payload)
    assert response.status_code == 404

    print(response.json())

def test_can_deactivate_user():
    user_id = 2
    header = {
        "x-actor-id": "1"
    }

    response = requests.delete(f"{USER_ENDPOINT}/{user_id}", headers=header)
    assert response.status_code == 204

    print(response.json())


def test_permission_error_on_deactivate_user():
    user_id = 1
    header = {
        "x-actor-id": "2"
    }

    response = requests.delete(f"{USER_ENDPOINT}/{user_id}", headers=header)
    assert response.status_code == 403

    print(response.json())

def test_value_error_on_deactivate_user():
    user_id = 999
    header = {
        "x-actor-id": "1"
    }

    response = requests.delete(f"{USER_ENDPOINT}/{user_id}", headers=header)
    assert response.status_code == 404

    print(response.json())

def test_can_reactivate_user():
    user_id = 2
    header = {
        "x-actor-id": "1"
    }

    response = requests.put(f"{USER_ENDPOINT}/{user_id}/reactivate", headers=header)
    assert response.status_code == 200

    data = response.json()
    print(data)

def test_permission_error_on_reactivate_user():
    user_id = 1
    header = {
        "x-actor-id": "2"
    }

    response = requests.put(f"{USER_ENDPOINT}/{user_id}/reactivate", headers=header)
    assert response.status_code == 403

    print(response.json())

def test_value_error_on_reactivate_user():
    user_id = 999
    header = {
        "x-actor-id": "1"
    }

    response = requests.put(f"{USER_ENDPOINT}/{user_id}/reactivate", headers=header)
    assert response.status_code == 404

    print(response.json())