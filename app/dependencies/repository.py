from typing import Callable, Type

from fastapi import Depends

from app.dependencies import get_db
from app.models import SessionLocal
from app.repositories.base import BaseRepository


def get_repository(
    repository_cls: Type[BaseRepository],
) -> Callable[[SessionLocal], BaseRepository]:
    def _get_repository(db_session: SessionLocal = Depends(get_db)) -> BaseRepository:
        return repository_cls(db_session)

    return _get_repository
