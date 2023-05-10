from sqlalchemy import select

from app.models import Tag
from app.repositories.base import BaseRepository


class TagRepository(BaseRepository):
    def get(self, id: int) -> Tag | None:
        stmt = select(Tag).where(Tag.id == id)
        return self.session.execute(stmt).scalars().first()

    def get_all(self) -> list[Tag]:
        stmt = select(Tag)
        return self.session.execute(stmt).scalars().all()
