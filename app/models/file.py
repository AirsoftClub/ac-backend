import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Table
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.utils import UUID


class File(Base):
    __tablename__ = "files"

    id = Column(UUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    path = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class HasFiles:
    @declared_attr
    def files(cls):
        files_association = Table(
            "%s_files" % cls.__tablename__,
            cls.metadata,
            Column("files_id", ForeignKey("files.id"), primary_key=True),
            Column(
                "%s_id" % cls.__tablename__,
                ForeignKey("%s.id" % cls.__tablename__),
                primary_key=True,
            ),
        )
        return relationship(File, secondary=files_association)
