from sqlalchemy.orm import Session, joinedload, selectinload
from models.sprint import Sprint, SprintStatus
from repositories.base_repository import BaseRepository
from models.task import Task

class SprintRepository(BaseRepository[Sprint]):
    def __init__(self, db: Session):
        super().__init__(Sprint, db)

    def find_active(self) -> list[Sprint]:
        return self.db.query(Sprint).filter(
            Sprint.status == SprintStatus.active
        ).all()

    def find_with_tasks_and_member(self, sprint_id: int) -> Sprint | None:
        return (self.db.query(Sprint)
                .options(joinedload(Sprint.tasks), joinedload(Sprint.members))
                .filter(Sprint.id == sprint_id)
                .first())
    
    def is_member(self, sprint_id: int, user_id: int) -> bool:
        sprint = self.find_by_id(sprint_id)
        if not sprint:
            return False
        return any(m.id == user_id for m in sprint.members) 

    def get_all_tasks_and_corresponding_member(self, sprint_id: int) -> Sprint | None:
        return (self.db.query(Sprint)
                .options(selectinload(Sprint.tasks).joinedload(Task.assignee))
                .filter(Sprint.id == sprint_id)
                .first())