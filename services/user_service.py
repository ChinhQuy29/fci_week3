from repositories.user_repository import UserRepository
from models.user import User, UserRole

class UserService:    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, name: str, email: str, role: UserRole = UserRole.member) -> User:
        if self.user_repo.email_exists(email):
            raise ValueError("Email already registered")
        user = User(name= name, email=email, role=role)
        return self.user_repo.save(user)

    def get(self, user_id: int) -> User:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        return user 
        
    def update(self, user_id: int, data: dict) -> User:
        user = self.get(user_id)
        for key, value in data.items():
            setattr(user, key, value)
        return self.user_repo.save(user)

    def deactivate(self, actor_id: int, user_id: int) -> User:
        actor = self.get(actor_id)
        if not actor.is_manager:
            raise PermissionError("Only managers can deactivate users")
        user = self.get(user_id)
        user.is_active = False
        return self.user_repo.save(user)

    def reactivate(self, actor_id: int, user_id: int) -> User:
        actor = self.get(actor_id)
        if not actor.is_manager:
            raise PermissionError("Only managers can reactivate users")
        user = self.get(user_id)
        user.is_active = True
        return self.user_repo.save(user)
    
    #sua loi nhay bac
    def find_all(self) -> list[User]:
        return self.user_repo.find_all()