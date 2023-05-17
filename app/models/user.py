from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.squad import squad_user


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    image = Column(String, nullable=True)

    is_admin = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    owned_fields = relationship("Field", back_populates="owner")
    squads = relationship("Squad", secondary=squad_user, back_populates="members")
    squad_leader = relationship("Squad", back_populates="leader")

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}({self.email})>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
