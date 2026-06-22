from sqlalchemy.orm import Session
from models.task import Task, TaskStatus
from repositories.base_repository import BaseRepository

class TaskRepository(BaseRepository[Task]):
    def __init__(self, db: Session):
        super().__init__(Task, db)

    def find_by_sprint(self, sprint_id: int) -> list[Task]:
        return self.db.query(Task).filter(Task.sprint_id == sprint_id).all()

    def find_by_assignee(self, assignee_id: int) -> list[Task]:
        return self.db.query(Task).filter(Task.assignee_id == assignee_id).all()

    def find_by_sprint_and_status(self, sprint_id: int, status: TaskStatus) -> list[Task]:
        return self.db.query(Task).filter(Task.sprint_id == sprint_id, Task.status == status).all()

    def find_by_status(self, status: TaskStatus) -> list[Task]:
        return self.db.query(Task).filter(Task.status == status).all()

    def find_unassigned(self, sprint_id: int) -> list[Task]:
        return self.db.query(Task).filter(Task.sprint_id == sprint_id, Task.assignee_id == None).all()
    
    
    

    
