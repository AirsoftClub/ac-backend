from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.models.base import Base

tag_field = Table(
    "tag_field",
    Base.metadata,
    Column("field_id", ForeignKey("fields.id")),
    Column("tag_id", ForeignKey("tags.id")),
)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    fields = relationship("Field", secondary=tag_field, back_populates="tags")

    def __repr__(self):
        return f"<Tag {self.description}>"
