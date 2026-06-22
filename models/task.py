from models.base_model import TimestampMixin
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from config.base import Base
import enum

class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

ALLOWED_TRANSITIONS = {
    TaskStatus.todo: {TaskStatus.in_progress},
    TaskStatus.in_progress: {TaskStatus.todo, TaskStatus.done},
    TaskStatus.done: set(),
}

class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(TimestampMixin, Base):
    sprint_id = Column(Integer, ForeignKey("sprints.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    is_completed = Column(Boolean, default=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.todo, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.low)
    
    sprint = relationship("Sprint", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")

    def can_transition_to(self, new_status: TaskStatus) -> bool:
        return new_status in ALLOWED_TRANSITIONS[self.status]

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', sprint_id={self.sprint_id}, assignee_id={self.assignee_id})>"