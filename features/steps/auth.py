from unittest import mock

import yaml
from behave import given, step
from behave.api.async_step import async_run_until_complete
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import select

from app.models import User
from app.services.jwt import JWTService
from tests.factories import UserFactory


@given("The JWT generates the following data")
def mock_auth(context):
    jwt_service = mock.Mock().return_value
    jwt_service.create_access_token.return_value = yaml.safe_load(context.text)
    context.app.dependency_overrides[JWTService] = lambda: jwt_service


@step("A user exists with the following data")
def create_user(context):
    data = yaml.safe_load(context.text)
    UserFactory(**data)


@step("I am logged with the email {email}")
@async_run_until_complete
async def login(context, email):
    stmt = select(User).where(User.email == email)
    user = (await context.session.execute(stmt)).scalars().first()
    if not user:
        raise Exception(f"User with email {email} does not exist")

    authorize = AuthJWT()
    access_token = authorize.create_access_token(user.email)
    context.headers = {"Authorization": f"Bearer {access_token}"}


@step("I set the {header_name} header to {header_value}")
def set_header(context, header_name, header_value):
    context.headers[header_name] = header_value
