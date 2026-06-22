from repositories.sprint_repository import SprintRepository
from repositories.user_repository import UserRepository
from models.sprint import Sprint, SprintStatus
from datetime import date

class SprintService:
    def __init__(self, sprint_repo: SprintRepository, user_repo: UserRepository):
        self.sprint_repo = sprint_repo
        self.user_repo = user_repo

    def create_sprint(self, creator_id: int, title: str, from_date: date, to_date: date) -> Sprint:
        creator = self.get_user(creator_id)
        if not creator.is_manager:
            raise PermissionError("Only managers can create sprints")
        
        if from_date > to_date:
            raise ValueError("to_date must be after from_date")
        
        sprint = Sprint(title=title, from_date=from_date, to_date=to_date, created_by=creator_id)
        return self.sprint_repo.save(sprint)

    def add_member(self, actor_id: int, member_id: int, sprint_id: int) -> Sprint:
        actor = self.get_user(actor_id)
        if not actor.is_manager:
            raise PermissionError("Only managers can add sprint members")
        
        sprint = self.get_sprint(sprint_id)
        member = self.get_user(member_id)
        if self.sprint_repo.is_member(sprint_id, member_id):
            raise ValueError("User is already a member of this sprint")
        
        sprint.members.append(member)
        return self.sprint_repo.save(sprint)

    def activate_sprint(self, actor_id: int,sprint_id: int) -> Sprint:
        actor = self.get_user(actor_id)
        if not actor.is_manager:
            raise PermissionError("Only managers can activate sprints")
        sprint = self.get_sprint(sprint_id)
        if sprint.status != SprintStatus.planned:
            raise ValueError("Only planned sprints can be activated")
        sprint.status = SprintStatus.active
        return self.sprint_repo.save(sprint)

    def close_sprint(self, actor_id: int, sprint_id: int) -> Sprint:
        actor = self.get_user(actor_id)
        if not actor.is_manager:
            raise PermissionError("Only managers can close sprints")
        sprint = self.get_sprint(sprint_id)
        if sprint.status != SprintStatus.active:
            raise ValueError("Only active sprints can be closed")
        sprint.status = SprintStatus.closed
        return self.sprint_repo.save(sprint)

    def get_user(self, user_id: int):
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID: {user_id} does not exist")
        return user

    def get_sprint(self, sprint_id: int):
        sprint = self.sprint_repo.find_by_id(sprint_id)
        if not sprint:
            raise ValueError(f"Sprint with ID: {sprint_id} does not exist")
        return sprint
    
    # sua loi nhay bac
    def find_all(self) -> list[Sprint]:
        return self.sprint_repo.find_all()
    
    def find_by_id(self, sprint_id: int) -> Sprint:
        return self.sprint_repo.find_by_id(sprint_id)
    
    def get_all_tasks_with_corresponding_member(self, sprint_id: int) -> Sprint:
        return self.sprint_repo.get_all_tasks_and_corresponding_member(sprint_id)