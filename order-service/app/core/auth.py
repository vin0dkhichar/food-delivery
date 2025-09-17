# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from pydantic import BaseModel
# from app.core.config import settings

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/users/login")


# class TokenData(BaseModel):
#     id: int
#     email: str
#     role: str


# def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
#         )
#         user_id: int = int(payload.get("sub"))
#         email: str = payload.get("email")
#         role: str = payload.get("role")
#         if user_id is None or email is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid token payload",
#             )
#         return TokenData(id=user_id, email=email, role=role)
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#         )


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
import requests
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/users/login")


class TokenData(BaseModel):
    id: int
    email: str
    role: str


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: int = int(payload.get("sub"))
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
            )

        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"http://localhost:8001/users/{user_id}", headers=headers)
        if resp.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or unauthorized in user service",
            )
        user_data = resp.json()
        return TokenData(
            id=user_data["id"], email=user_data["email"], role=user_data["role"]
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
