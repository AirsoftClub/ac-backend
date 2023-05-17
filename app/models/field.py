from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.tag import tag_field


class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    latitude = Column(Numeric(precision=9), nullable=True)
    longitude = Column(Numeric(precision=9), nullable=True)

    # Relationship
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="owned_fields")
    tags = relationship("Tag", secondary=tag_field, back_populates="fields")

    @property
    def is_active(self) -> bool:
        return self.deleted_at is None

    def __repr__(self):
        return f"<Field {self.name}>"
