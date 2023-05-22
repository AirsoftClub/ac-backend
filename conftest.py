import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import Settings
from app.dependencies import get_current_user, get_db
from app.models import Base
from main import create_app
from tests.factories import UserFactory, sqlalchemy_factories


@pytest.fixture(name="settings")
def test_settings():
    return Settings(DATABASE={"URL": "sqlite:///:memory:"})


@pytest.fixture(autouse=True)
def db_session(settings):
    engine = create_engine(
        settings.DATABASE.URL, connect_args={"check_same_thread": False}
    )

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return SessionLocal()


@pytest.fixture
def app(db_session):
    app = create_app()
    app.dependency_overrides[get_db] = lambda: db_session
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def url_for(app):
    return app.url_path_for


@pytest.fixture(autouse=True)
def register_sqlalchemy_factory(db_session):
    for sqlalchemy_factory in sqlalchemy_factories:
        sqlalchemy_factory._meta.sqlalchemy_session = db_session


@pytest.fixture
def authenticate_user(app):
    user = UserFactory()
    app.dependency_overrides[get_current_user] = lambda: user
    return user
