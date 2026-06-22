from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session
from config.base import Base

T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def find_by_id(self, id: int) -> T | None:
        return self.db.get(self.model, id)
    
    def find_all(self) -> list[T]:
        return self.db.query(self.model).all()
    
    def save(self, obj: T) -> T:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def delete(self, id: int) -> None:
        obj = self.find_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            