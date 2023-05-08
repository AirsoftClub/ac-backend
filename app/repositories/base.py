from app.models import SessionLocal


class BaseRepository:
    def __init__(self, session: SessionLocal):
        self.session = session
