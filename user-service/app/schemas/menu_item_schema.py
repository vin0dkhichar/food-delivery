from pydantic import BaseModel
from typing import Optional


class MenuItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True


class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    is_available: bool
    restaurant_id: int

    class Config:
        from_attributes = True
