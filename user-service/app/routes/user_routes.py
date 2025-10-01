from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.core.dependencies import get_current_user
from app.models.user import User
from app.core.logger import logger


class UserRoutes:
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["Users"])
        self.user_service = UserService(UserRepository())

        self.router.add_api_route(
            "/",
            self.register,
            response_model=UserResponse,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
        )

        self.router.add_api_route(
            "/login",
            self.login,
            status_code=status.HTTP_200_OK,
            methods=["POST"],
        )

        self.router.add_api_route(
            "/me",
            self.get_current_user,
            response_model=UserResponse,
            methods=["GET"],
        )

    def register(self, user_data: UserCreate, db: Session = Depends(get_db)):
        logger.info("Start register email=%s", user_data.email)
        try:
            return self.user_service.create_user(db, user_data)
        except ValueError as e:
            logger.error("Register error: %s", str(e))
            raise HTTPException(status_code=400, detail=str(e))

    def login(
        self,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
    ):
        logger.info("Start login username=%s", form_data.username)

        token = self.user_service.authenticate_user(
            db, form_data.username, form_data.password
        )
        if not token:
            logger.error("Invalid login attempt username=%s", form_data.username)
            raise HTTPException(status_code=401, detail="Invalid credentials")

        logger.debug("Login success username=%s", form_data.username)
        return {"access_token": token, "token_type": "bearer"}

    def get_current_user(
        self,
        current_user: User = Depends(get_current_user),
    ):
        logger.info("Fetching current user id=%s", current_user.id)
        return current_user
