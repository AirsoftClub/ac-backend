from tempfile import TemporaryDirectory

import respx
from behave import fixture, use_fixture
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import Settings
from app.dependencies import get_db, get_settings
from app.models import Base
from main import create_app
from tests.factories import sqlalchemy_factories


def init_db(context):
    context.engine = create_engine(
        context.settings.DATABASE.URL, connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=context.engine)

    Base.metadata.drop_all(bind=context.engine)
    Base.metadata.create_all(bind=context.engine)

    context.session = SessionLocal()


def init_app(context):
    app = create_app()
    app.dependency_overrides[get_db] = lambda: context.session
    app.dependency_overrides[get_settings] = lambda: context.settings
    context.app = app


def init_test_client(context):
    context.client = TestClient(context.app)


@fixture
def init_http_mock(context):
    respx.mock.start()
    yield
    respx.mock.stop()


def register_sqlalchemy_factory(context):
    for sqlalchemy_factory in sqlalchemy_factories:
        sqlalchemy_factory._meta.sqlalchemy_session = context.session


def before_all(context):
    context.temp_dir = TemporaryDirectory()
    context.settings = Settings(
        DATABASE={"URL": "sqlite:///./test.db"}, STATIC_FOLDER=context.temp_dir.name
    )


def before_scenario(context, scenario):
    init_http_mock(context)
    init_db(context)
    init_app(context)
    register_sqlalchemy_factory(context)
    init_test_client(context)
    use_fixture(init_http_mock, context)

    context.headers = {}
