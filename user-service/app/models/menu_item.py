from sqlalchemy import Integer, String, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship, mapped_column
from datetime import datetime, timezone

from app.core.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, nullable=False)
    description = mapped_column(String, nullable=True)
    price = mapped_column(Float, nullable=False)
    is_available = mapped_column(Boolean, default=True)

    category = mapped_column(String, nullable=True, index=True)
    cuisine_type = mapped_column(String, nullable=True, index=True)
    tags = mapped_column(JSON, nullable=True, default=[])

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

    restaurant_id = mapped_column(Integer, ForeignKey("restaurants.id"), nullable=False)
    image_id = mapped_column(
        Integer, ForeignKey("storage_file.id"), nullable=True, index=True
    )

    restaurant = relationship("Restaurant", back_populates="menu_items")
    image = relationship("StorageFileORM", back_populates="menu_items")
