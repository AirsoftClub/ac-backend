from sqlalchemy import select

from app.models import Field, Tag
from app.repositories.base import BaseRepository


class FieldRepository(BaseRepository):
    def get_all(self) -> list[Field]:
        stmt = select(Field).where(Field.deleted_at.is_(None))
        return self.session.execute(stmt).scalars().all()

    def get_by_tag(self, tag_id: int) -> list[Field]:
        stmt = select(Field).where(Field.tags.any(Tag.id == tag_id))
        return self.session.execute(stmt).scalars().all()
