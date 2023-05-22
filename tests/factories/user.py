from factory import LazyAttribute
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyText
from pytest_factoryboy import register

from app.models.user import User


@register
class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    first_name = FuzzyText()
    last_name = FuzzyText()
    email = LazyAttribute(lambda k: f"{k.first_name}_{k.last_name}@example.com")
    deleted_at = None
