from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/users/login")


class TokenData(BaseModel):
    id: int
    email: str
    role: str
    full_name: str
    phone_number: str


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return TokenData(
            id=int(payload.get("sub")),
            email=payload.get("email"),
            role=payload.get("role"),
            full_name=payload.get("full_name"),
            phone_number=payload.get("phone_number"),
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
