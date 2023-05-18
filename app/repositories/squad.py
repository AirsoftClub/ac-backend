from sqlalchemy import select

from app.core.exceptions import ResourceNotFound, Unauthorized
from app.models import Squad, User
from app.repositories.base import BaseRepository


class SquadRepository(BaseRepository):
    def get_all(self) -> list[Squad]:
        stmt = select(Squad).where(Squad.deleted_at.is_(None))
        return self.session.execute(stmt).scalars().all()

    def get(self, squad_id: int) -> Squad | None:
        stmt = (
            select(Squad).where(Squad.id == squad_id).where(Squad.deleted_at.is_(None))
        )
        squad = self.session.execute(stmt).scalars().first()
        if not squad:
            raise ResourceNotFound("Squad")
        return squad

    def add_member(self, squad_id: int, current_user: User, user: User) -> None:
        squad = self.get(squad_id)

        if not squad:
            raise ResourceNotFound("Squad")

        if squad.leader != current_user:
            raise Unauthorized

        squad.members.append(user)
        self.session.add(squad)
        self.session.commit()