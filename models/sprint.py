from models.base_model import TimestampMixin
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.orm import relationship
from config.base import Base
import enum

class SprintStatus(str, enum.Enum):
    planned = "planned"
    active = "active"
    closed = "closed"

class Sprint(TimestampMixin, Base):
    from_date = Column(DateTime, nullable=False)
    to_date = Column(DateTime, nullable=False)
    title = Column(String(255), nullable=False)
    status = Column(Enum(SprintStatus), default=SprintStatus.planned)
    
    tasks = relationship("Task", back_populates="sprint", cascade="all, delete-orphan")
    members = relationship("User", secondary="sprint_members", back_populates="sprints")

    def __repr__(self):
        return f"<Sprint(id={self.id}, title='{self.title}', from_date={self.from_date}, to_date={self.to_date})>"