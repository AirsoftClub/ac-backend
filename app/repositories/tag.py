from sqlalchemy import select

from app.models import Tag
from app.repositories.base import BaseRepository


class TagRepository(BaseRepository):
    async def get(self, id: int) -> Tag | None:
        stmt = select(Tag).where(Tag.id == id)
        return (await self.session.execute(stmt)).scalars().first()

    async def get_all(self) -> list[Tag]:
        stmt = select(Tag)
        return (await self.session.execute(stmt)).scalars().all()
