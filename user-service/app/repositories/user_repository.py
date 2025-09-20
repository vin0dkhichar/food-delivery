from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def create_user(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_user_by_phone(self, db: Session, phone_number: str) -> Optional[User]:
        if not phone_number:
            return None
        return db.query(User).filter(User.phone_number == phone_number).first()

    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()
