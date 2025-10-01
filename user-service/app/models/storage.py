from sqlalchemy import Integer, String, Boolean, ForeignKey, Column, DateTime
from sqlalchemy.orm import relationship, mapped_column
from datetime import datetime, timezone

from app.core.database import Base


class StorageBackendORM(Base):
    __tablename__ = "storage_backend"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False, index=True)
    backend_type = mapped_column(
        String, nullable=False, index=True, default="amazon_s3"
    )

    aws_host = mapped_column(String, nullable=True)
    aws_bucket = mapped_column(String, nullable=False)
    aws_access_key_id = mapped_column(String, nullable=False)
    aws_secret_access_key = mapped_column(String, nullable=False)
    aws_region = mapped_column(String, nullable=True)
    aws_file_acl = mapped_column(String, nullable=True, default="public-read")

    active = mapped_column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    documents = relationship("StorageFileORM", back_populates="backend")


class StorageFileORM(Base):
    __tablename__ = "storage_file"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False, index=True)
    relative_path = mapped_column(String, nullable=True)
    file_size = mapped_column(Integer, nullable=True)
    checksum = mapped_column(String(64), nullable=True, index=True)
    mimetype = mapped_column(String, nullable=True)
    extension = mapped_column(String, nullable=True)
    is_active = mapped_column(Boolean, default=True)

    public_url = Column(String(1000), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    backend_id = mapped_column(ForeignKey("storage_backend.id"), nullable=False)

    backend = relationship("StorageBackendORM", back_populates="documents")
    menu_items = relationship("MenuItem", back_populates="image")
