from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=True)
    address = Column(String, nullable=False)
    phone_number = Column(String, nullable=True, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", backref="restaurants")
    menu_items = relationship("MenuItem", back_populates="restaurant", cascade="all, delete")

