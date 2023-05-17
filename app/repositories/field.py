from sqlalchemy import func, select

from app.models import Field, Tag
from app.repositories.base import BaseRepository


class FieldRepository(BaseRepository):
    def get_all(self) -> list[Field]:
        stmt = (
            select(Field)
            .where(Field.deleted_at.is_(None))
            .order_by(Field.created_at.desc())
        )
        return self.session.execute(stmt).scalars().all()

    def get(self, id: int) -> Field | None:
        stmt = select(Field).where(Field.id == id)
        return self.session.execute(stmt).scalars().first()

    def get_by_tag(self, tag_id: int) -> list[Field]:
        stmt = select(Field).where(Field.tags.any(Tag.id == tag_id))
        return self.session.execute(stmt).scalars().all()

    def get_all_by_distance(
        self, latitude: float, longitude: float
    ) -> list[tuple[Field, float]]:
        distance = (
            func.acos(
                func.sin(func.radians(latitude))
                * func.sin(func.radians(Field.latitude))
                + func.cos(func.radians(latitude))
                * func.cos(func.radians(Field.latitude))
                * func.cos(func.radians(longitude) - func.radians(Field.longitude))
            )
            * 6371  # Earth's radius in kilometers
        )

        stmt = (
            select(Field, distance.label("distance"))
            .where(Field.deleted_at.is_(None))
            .order_by(distance.asc())
        )
        return self.session.execute(stmt).all()
