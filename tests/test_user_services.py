import pytest

from ..services.user_service import register, get, update, deactivate, reactivate, find_all

def test_register_user():
    user = register("John Doe", "john.doe@example.com", "member")
    assert user.name == "John Doe"
    assert user.email == "john.doe@example.com"
    assert user.role == "member"

def test_register_existing_email():
    register("Jane Doe", "jane.doe@example.com", "member")
    with pytest.raises(ValueError):
        register("John Smith", "jane.doe@example.com", "member")
    
def test_get_user():
    user = register("Alice", "alice@example.com", "member")
    retrieved_user = get(user.id)
    assert retrieved_user.id == user.id

def test_user_not_found():
    with pytest.raises(ValueError):
        get(999)

def test_update_user():
    user = register("Bob", "bob@example.com", "member")
    updated_user = update(user.id, {"name": "Bobby"})
    assert updated_user.name == "Bobby"

def test_deactivate_user():
    manager = register("Manager", "manager@example.com", "manager")
    user = register("Charlie", "charlie@example.com", "member")
    deactivated_user = deactivate(manager.id, user.id)
    assert not deactivated_user.is_active

def test_deactivate_user_permission_error():
    user = register("David", "david@example.com", "member")
    another_user = register("Eve", "eve@example.com", "member")
    with pytest.raises(PermissionError):
        deactivate(user.id, another_user.id)

def test_reactivate_user():
    manager = register("Manager2", "manager2@example.com", "manager")
    user = register("Frank", "frank@example.com", "member")
    deactivate(manager.id, user.id)
    reactivated_user = reactivate(manager.id, user.id)
    assert reactivated_user.is_active

def test_reactivate_user_permission_error():
    user = register("Grace", "grace@example.com", "member")
    another_user = register("Heidi", "heidi@example.com", "member")
    deactivate(register("Manager3", "manager3@example.com", "manager").id, user.id)
    with pytest.raises(PermissionError):
        reactivate(user.id, another_user.id)

def test_find_all_users():
    register("Ivan", "ivan@example.com", "member")
    register("Judy", "judy@example.com", "member")
    users = find_all()
    assert len(users) >= 2

    