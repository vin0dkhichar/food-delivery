from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RestaurantCreate(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    phone_number: Optional[str] = None


class RestaurantResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    address: str
    phone_number: Optional[str]
    owner_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
