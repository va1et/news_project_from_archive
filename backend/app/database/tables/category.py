import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table, func
from sqlalchemy.dialects.postgresql import UUID

from app.database.connection import Base

news_category = Table(
    "news_category",
    Base.metadata,
    Column("news_guid", UUID(as_uuid=True), ForeignKey("news.guid")),
    Column("category_guid", UUID(as_uuid=True), ForeignKey("category.guid")),
)


class Category(Base):
    __tablename__ = "category"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False, unique=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
