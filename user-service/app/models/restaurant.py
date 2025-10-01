from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, Float, JSON
from sqlalchemy.orm import relationship, mapped_column
from datetime import datetime, timezone

from app.core.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, nullable=False, unique=True, index=True)
    description = mapped_column(String, nullable=True)
    address = mapped_column(String, nullable=False)
    phone_number = mapped_column(String, nullable=True, unique=True)
    owner_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
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

    category = mapped_column(String, nullable=True, index=True)
    cuisine_type = mapped_column(String, nullable=True, index=True)
    tags = mapped_column(JSON, nullable=True, default=[])

    latitude = mapped_column(Float, nullable=True, index=True)
    longitude = mapped_column(Float, nullable=True, index=True)

    owner = relationship("User", backref="restaurants")
    menu_items = relationship(
        "MenuItem", back_populates="restaurant", cascade="all, delete"
    )
