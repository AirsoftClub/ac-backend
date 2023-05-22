from tests.factories.field import FieldFactory
from tests.factories.squad import SquadFactory
from tests.factories.tag import TagFactory
from tests.factories.user import UserFactory

sqlalchemy_factories = [UserFactory, FieldFactory, TagFactory, SquadFactory]


__all__ = [
    "FieldFactory",
    "SquadFactory",
    "TagFactory",
    "UserFactory",
    "sqlalchemy_factories",
]
