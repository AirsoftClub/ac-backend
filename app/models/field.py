from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.models.base import Base

association_table = Table(
    "association_table",
    Base.metadata,
    Column("field_id", ForeignKey("fields.id")),
    Column("tag_id", ForeignKey("tags.id")),
)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    description = Column(String, unique=True)
    fields = relationship("Field", secondary=association_table, back_populates="tags")


class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)

    # Relationship
    tags = relationship("Field", secondary=association_table, back_populates="tags")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="fields")

    @property
    def is_active(self) -> bool:
        return self.deleted_at is None
