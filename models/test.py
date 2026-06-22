from models.base_model import TimestampMixin
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.orm import relationship
from config.base import Base
import enum

class Test(TimestampMixin, Base):
    pass