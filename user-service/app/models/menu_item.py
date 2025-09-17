from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)

    restaurant = relationship("Restaurant", back_populates="menu_items")
