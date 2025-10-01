from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    role: UserRole = UserRole.CUSTOMER
    delivery_radius_km: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    role: UserRole    
    delivery_radius_km: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True
