from pydantic import BaseModel
from typing import Optional, List


class MenuItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True
    category: Optional[str] = None
    cuisine_type: Optional[str] = None
    tags: Optional[List[str]] = []
    restaurant_id: int
    image_id: Optional[int] = None


class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    is_available: bool
    category: Optional[str]
    cuisine_type: Optional[str]
    tags: Optional[List[str]]
    restaurant_id: int
    image_id: Optional[int] 

    class Config:
        from_attributes = True
