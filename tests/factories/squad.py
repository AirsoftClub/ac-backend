from factory import SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyText

from app.models import Squad
from tests.factories.user import UserFactory


class SquadFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Squad
        sqlalchemy_session_persistence = "commit"

    name = FuzzyText()
    emblem = FuzzyText()
    leader = SubFactory(UserFactory)
