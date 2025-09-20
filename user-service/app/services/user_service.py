from typing import Optional
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, db: Session, user_data: UserCreate) -> User:
        if self.repository.get_user_by_email(db, user_data.email):
            raise ValueError("email_exists")
        if user_data.phone_number and self.repository.get_user_by_phone(
            db, user_data.phone_number
        ):
            raise ValueError("phone_exists")

        hashed_password = hash_password(user_data.password)
        new_user = User(
            email=user_data.email,
            password_hash=hashed_password,
            full_name=user_data.full_name,
            phone_number=user_data.phone_number,
            address=user_data.address,
            role=user_data.role,
            is_active=True,
        )
        return self.repository.create_user(db, new_user)

    def authenticate_user(
        self, db: Session, username: str, password: str
    ) -> Optional[str]:
        """
        Returns a JWT access token (string) on success, or None on failure.
        """
        user = self.repository.get_user_by_email(db, username)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        token = create_access_token(user)
        return token

    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return self.repository.get_user_by_id(db, user_id)
