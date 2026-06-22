from models.base_model import TimestampMixin
from sqlalchemy import Column, Boolean, String, Enum
from sqlalchemy.orm import relationship, validates
from config.base import Base
import enum

class UserRole(str, enum.Enum):
    member = "member"
    manager = "manager"

class User(TimestampMixin, Base):
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(Enum(UserRole), default=UserRole.member, nullable=False)
    is_active = Column(Boolean, default=True)
    
    sprints = relationship("Sprint", secondary="sprint_members", back_populates="members")
    tasks = relationship("Task", back_populates="assignee", cascade="all, delete-orphan")

    @validates("email")
    def validate_email(self, key, value):
        if "@" not in value:
            raise ValueError("Invalid email")
        return value.lower()

    def __repr__(self):
        return f"<User(id={self.id}, role='{self.role}')>"

    @property
    def is_manager(self) -> bool:
        return self.role == UserRole.manager