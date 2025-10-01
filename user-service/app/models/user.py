from sqlalchemy import Integer, String, Boolean, Enum, DateTime, Float
from sqlalchemy.orm import mapped_column
from datetime import datetime, timezone
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    DELIVERY_AGENT = "delivery_agent"
    RESTAURANT = "restaurant"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    email = mapped_column(String, unique=True, nullable=False, index=True)
    password_hash = mapped_column(String, nullable=False)
    full_name = mapped_column(String, nullable=False)
    phone_number = mapped_column(String(20), nullable=True, unique=True, index=True)
    address = mapped_column(String, nullable=True)
    role = mapped_column(Enum(UserRole), default=UserRole.CUSTOMER)
    is_active = mapped_column(Boolean, default=True)

    created_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deleted_at = mapped_column(DateTime(timezone=True), nullable=True)

    delivery_radius_km = mapped_column(Integer, nullable=True)
    latitude = mapped_column(Float, nullable=True, index=True)
    longitude = mapped_column(Float, nullable=True, index=True)
