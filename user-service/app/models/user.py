from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from datetime import datetime
import enum
from app.core.database import Base


class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    DELIVERY_AGENT = "delivery_agent"
    RESTAURANT = "restaurant"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True, unique=True)
    address = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
