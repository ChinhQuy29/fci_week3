from sqlalchemy import Column, Integer, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import declared_attr


class TimestampMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    updated_by = Column(Integer, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"

