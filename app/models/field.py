from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.models.base import Base

association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("fields.id")),
    Column("right_id", ForeignKey("tags.id")),
)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    description = Column(String)
    fields = relationship("Field", secondary=association_table, back_populates="tags")


class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    tags = relationship("Field", secondary=association_table, back_populates="tags")

    @property
    def is_active(self):
        return self.deleted_at is None
