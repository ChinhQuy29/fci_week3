from sqlalchemy import Table, Column, Integer, ForeignKey
from config.base import Base

sprint_users = Table(
    "sprint_members",
    Base.metadata,
    Column("sprint_id", Integer, ForeignKey("sprints.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True)
)