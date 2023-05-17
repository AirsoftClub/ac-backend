from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.models.base import Base

squad_user = Table(
    "squad_user",
    Base.metadata,
    Column("squad_id", ForeignKey("squads.id")),
    Column("user_id", ForeignKey("users.id")),
)


class Squad(Base):
    __tablename__ = "squads"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True, index=True)
    emblem = Column(String, nullable=True, unique=True)
    members = relationship("User", secondary=squad_user, back_populates="squads")
    leader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    leader = relationship("User", back_populates="squad_leader")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Squad {self.name}>"
