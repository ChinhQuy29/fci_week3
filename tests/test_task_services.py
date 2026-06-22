import pytest

from ..services.task_service import create_task, assign_task, unassign_task, start_task, finish_task, transition_task, get_board, get_task, find_by_sprint, find_by_id, get_all_tasks


def test_create_task():
    task = create_task(1, 1, "Task 1", "Description 1", "high")
    assert task.title == "Task 1"
    assert task.description == "Description 1"
    assert task.priority == "high"
    assert task.sprint_id == 1

def test_permission_error_on_create_task():
    with pytest.raises(PermissionError):
        create_task(2, 1, "Task 2", "Description 2", "medium")

def test_assign_task():
    task = create_task(1, 1, "Task 3", "Description 3", "low")
    assigned_task = assign_task(1, task.id, 3)
    assert assigned_task.assignee_id == 3

def test_permission_error_on_assign_task():
    task = create_task(1, 1, "Task 4", "Description 4", "medium")
    with pytest.raises(PermissionError):
        assign_task(2, task.id, 3)

def test_value_error_on_assign_task():
    task = create_task(1, 1, "Task 5", "Description 5", "high")
    with pytest.raises(ValueError):
        assign_task(1, task.id, 999)

def test_unassign_task():
    task = create_task(1, 1, "Task 6", "Description 6", "low")
    assign_task(1, task.id, 3)
    unassigned_task = unassign_task(1, task.id)
    assert unassigned_task.assignee_id is None

def test_permission_error_on_unassign_task():
    task = create_task(1, 1, "Task 7", "Description 7", "medium")
    assign_task(1, task.id, 3)
    with pytest.raises(PermissionError):
        unassign_task(2, task.id)

def test_start_task():
    task = create_task(1, 1, "Task 8", "Description 8", "high")
    assign_task(1, task.id, 3)
    started_task = start_task(3, task.id)
    assert started_task.status == "in_progress"

def test_finish_task():
    task = create_task(1, 1, "Task 9", "Description 9", "low")
    assign_task(1, task.id, 3)
    start_task(3, task.id)
    finished_task = finish_task(3, task.id)
    assert finished_task.status == "done"

def test_transition_task():
    task = create_task(1, 1, "Task 10", "Description 10", "medium")
    assign_task(1, task.id, 3)
    transitioned_task = transition_task(3, task.id, "in_progress")
    assert transitioned_task.status == "in_progress"

def test_permission_error_on_transition_task():
    task = create_task(1, 1, "Task 11", "Description 11", "high")
    assign_task(1, task.id, 3)
    with pytest.raises(PermissionError):
        transition_task(2, task.id, "in_progress")

def test_value_error_on_transition_task():
    task = create_task(1, 1, "Task 12", "Description 12", "low")
    assign_task(1, task.id, 3)
    with pytest.raises(ValueError):
        transition_task(3, task.id, "done")

def test_get_board():
    board = get_board(1)
    assert board is not None

def test_get_task():
    task = get_task(1)
    assert task is not None

def test_get_task_not_found():
    with pytest.raises(ValueError):
        get_task(999)

def test_find_by_sprint():
    tasks = find_by_sprint(1)
    assert tasks is not None

def test_find_by_sprint_no_tasks():
    tasks = find_by_sprint(999)
    assert tasks == []

def test_find_by_id():
    task = find_by_id(1)
    assert task is not None

def test_find_by_id_not_found():
    with pytest.raises(ValueError):
        find_by_id(999)

def test_get_all_tasks():
    tasks = get_all_tasks()
    assert tasks is not None
