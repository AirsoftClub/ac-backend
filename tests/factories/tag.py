from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyText

from app.models import Tag


class TagFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Tag
        sqlalchemy_session_persistence = "commit"

    description = FuzzyText()
