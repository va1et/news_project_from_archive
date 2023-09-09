import uuid

from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base
from app.database.tables import news_category


class News(Base):
    __tablename__ = "news"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    likes = Column(Integer, default=0)
    comments = relationship("Comment", back_populates="news", lazy="joined", uselist=True)
    media = relationship("Media", back_populates="news", lazy="joined", uselist=True)
    categories = relationship("Category", secondary=news_category, lazy="joined", uselist=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
