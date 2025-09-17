from datetime import datetime
from typing import List
from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int
    price: float


class OrderCreate(BaseModel):
    restaurant_id: int
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
