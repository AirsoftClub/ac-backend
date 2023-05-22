from factory import List, SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyFloat, FuzzyText
from pytest_factoryboy import register

from app.models import Field
from tests.factories.tag import TagFactory


@register
class FieldFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Field
        sqlalchemy_session_persistence = "commit"

    name = FuzzyText()
    description = FuzzyText()
    deleted_at = None
    owner = None
    tags = List([SubFactory(TagFactory) for _ in range(5)])
    latitude = FuzzyFloat(low=-90, high=90, precision=9)
    longitude = FuzzyFloat(low=-90, high=90, precision=9)
