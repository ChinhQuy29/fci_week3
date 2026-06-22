from sqlalchemy.orm import Session
from repositories.base_repository import BaseRepository
from models.user import User
from sqlalchemy import or_, func

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def find_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email.lower()).first()

    def email_exists(self, email: str) -> bool:
        return self.db.query(User).filter(User.email == email.lower()).first() is not None

    def search(self, keyword: str) -> list[User]:
        term = f"%{keyword.lower()}%"
        return self.db.query(User).filter(
            or_(func.lower(User.name).like(term),
                func.lower(User.email).like(term))
        ).all()