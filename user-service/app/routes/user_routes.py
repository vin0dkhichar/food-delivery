from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService(UserRepository())


@router.post("/", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db, user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    token = user_service.authenticate_user(db, form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this user"
        )
    return current_user
