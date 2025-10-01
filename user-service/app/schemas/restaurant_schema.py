from typing import Optional
from pydantic import BaseModel


class RestaurantCreate(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    phone_number: Optional[str] = None
    category: Optional[str] = None
    cuisine_type: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    tags: Optional[list[str]] = None


class RestaurantResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    address: str
    phone_number: Optional[str]
    category: Optional[str]
    cuisine_type: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    tags: Optional[list[str]] = None

    class Config:
        from_attributes = True
