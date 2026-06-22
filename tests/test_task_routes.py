import requests
from dotenv import load_dotenv
import os

load_dotenv()

TASK_ENDPOINT = os.getenv("TASK_ENDPOINT")

def test_can_list_tasks_by_sprint():
    sprint_id = 1

    response = requests.get(f"{TASK_ENDPOINT}/sprint/{sprint_id}")
    assert response.status_code == 200

    data = response.json()
    print(data)

def test_can_get_task():
    task_id = 1

    response = requests.get(f"{TASK_ENDPOINT}/{task_id}")
    assert response.status_code == 200

    data = response.json()
    print(data)

def test_task_not_found():
    task_id = 999  # Assuming this task ID does not exist

    response = requests.get(f"{TASK_ENDPOINT}/{task_id}")
    assert response.status_code == 404

    print(response.json())

def test_can_get_board():
    sprint_id = 1

    response = requests.get(f"{TASK_ENDPOINT}/sprint/{sprint_id}/board")
    assert response.status_code == 200

    data = response.json()
    print(data)

def test_can_create_task():
    payload = {
        "title": "New Task",
        "description": "This is a new task.",
        "sprint_id": 1
    }

    header = {
        "x-actor-id": "1"
    }

    response = requests.post(TASK_ENDPOINT, json=payload, headers=header)
    assert response.status_code == 201

    data = response.json()
    print(data)

def test_permission_error_on_create_task():
    payload = {
        "title": "New Task 2",
        "description": "This is a new task.",
        "sprint_id": 2
    }

    header = {
        'x-actor-id': "2"
    }

    response = requests.post(TASK_ENDPOINT, json=payload, headers=header)
    assert response.status_code == 403

    data = response.json()
    print(data)

def test_value_error_on_create_task():
    payload = {
        "title": "abc" * 100,
        "description": "Fault",
        "sprint_id": 1
    }

    header = {
        'x-actor-id': "1"
    }

    response = requests.post(TASK_ENDPOINT, json=payload, headers=header)
    assert response.status_code == 400

    data = response.json()
    print(data)

def test_can_assign_task():
    task_id = 1
    
    payload = {
        "assignee_id": 2
    }

    header = {
        "x-actor-id": "1"
    }

    response = requests.put(f"{TASK_ENDPOINT}/{task_id}/assign", json=payload, headers=header)
    assert response.status_code == 200

    data = response.json()
    print(data)

def test_permission_error_on_assign_task():
    task_id = 1

    payload = {
        "assignee_id": 2
    }

    header = {
        "x-actor-id": "3"
    }

    response = requests.put(f"{TASK_ENDPOINT}/{task_id}/assign", json=payload, headers=header)
    assert response.status_code == 403

    print(response.json())

def test_value_error_on_assign_task():
    task_id = 999

    payload = {
        "assignee_id": 2
    }

    header = {
        "x-actor-id": "1"
    }

    response = requests.put(f"{TASK_ENDPOINT}/{task_id}/assign", json=payload, headers=header)
    assert response.status_code == 400

    print(response.json())

def test_can_unassign_task():
    task_id = 1

    header = {
        "x-actor-id": "1"
    }

    response = requests.put(f"{TASK_ENDPOINT}/{task_id}/unassign", headers=header)
    assert response.status_code == 201

    print(response.json())


def test_permission_error_on_unassign_task():
    task_id = 1

    header = {
        "x-actor-id": "3"
    }

    response = requests.put(f"{TASK_ENDPOINT}/{task_id}/unassign", headers=header)
    assert response.status_code == 403

    print(response.json())

def test_value_error_on_unassign_task():
    task_id = 999

    header = {
        "x-actor-id": "1"
    }

    response = requests.put(f"{TASK_ENDPOINT}/{task_id}/unassign", headers=header)
    assert response.status_code == 400

    print(response.json())

def test_can_start_task():
    task_id = 1

    header = {
        "x-actor-id": "1"
    }

    response = requests.put(f"{TASK_ENDPOINT}/{task_id}/start", headers=header)
    assert response.status_code == 201

    print(response.json())

def test_permission_error_on_start_task():
    task_id = 1

    header = {
        "x-actor-id": "3"
    }

    response = requests.put(f"{TASK_ENDPOINT}/{task_id}/start", headers=header)
    assert response.status_code == 403

    print(response.json())

def test_value_error_on_start_task():
    task_id = 999

    header = {
        "x-actor-id": "1"
    }

    response = requests.put(f"{TASK_ENDPOINT}/{task_id}/start", headers=header)
    assert response.status_code == 400

    print(response.json())

def test_can_finish_task():
    task_id = 1

    header = {
        "x-actor-id": "1"
    }

    response = requests.put(f"{TASK_ENDPOINT}/{task_id}/finish", headers=header)
    assert response.status_code == 201

    print(response.json())

def test_permission_error_on_finish_task():
    task_id = 1

    header = {
        "x-actor-id": "3"
    }

    response = requests.put(f"{TASK_ENDPOINT}/{task_id}/finish", headers=header)
    assert response.status_code == 403

    print(response.json())

def test_value_error_on_finish_task():
    task_id = 999

    header = {
        "x-actor-id": "1"
    }

    response = requests.put(f"{TASK_ENDPOINT}/{task_id}/finish", headers=header)
    assert response.status_code == 400

    print(response.json())

def test_can_update_status():
    task_id = 1

    payload = {
        "status": "in_progress"
    }

    header = {
        "x-actor-id": "1"
    }

    response = requests.put(f"{TASK_ENDPOINT}/{task_id}/status", json=payload, headers=header)
    assert response.status_code == 200

    data = response.json()
    print(data)

def test_permission_error_on_update_status():
    task_id = 1

    payload = {
        "status": "in_progress"
    }

    header = {
        "x-actor-id": "3"
    }

    response = requests.put(f"{TASK_ENDPOINT}/{task_id}/status", json=payload, headers=header)
    assert response.status_code == 403

    print(response.json())

def test_value_error_on_update_status():
    task_id = 999

    payload = {
        "status": "in_progress"
    }

    header = {
        "x-actor-id": "1"
    }

    response = requests.put(f"{TASK_ENDPOINT}/{task_id}/status", json=payload, headers=header)
    assert response.status_code == 400

    print(response.json())

def test_can_list_all_tasks():
    response = requests.get(TASK_ENDPOINT)
    assert response.status_code == 200

    data = response.json()
    print(data)

def test_can_create_task_from_movie():
    header = {
        "x-actor-id": "1"
    }

    response = requests.post(f"{TASK_ENDPOINT}/movie", headers=header)
    assert response.status_code == 201

    data = response.json()
    print(data)