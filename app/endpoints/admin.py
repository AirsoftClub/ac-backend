from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend

from app.core.settings import settings
from app.models import Field, File, Squad, Tag, User, engine


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if username == settings.ADMIN.USER and password == settings.ADMIN.PASSWORD:
            request.session.update({"token": "logged"})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")
        if not token or token != "logged":
            return RedirectResponse(request.url_for("admin:login"), status_code=302)


class UserAdmin(ModelView, model=User):
    column_list = [
        User.email,
        User.first_name,
        User.last_name,
        User.is_admin,
        User.squads,
    ]


class FieldAdmin(ModelView, model=Field):
    column_list = [Field.name, Field.owner, Field.tags]


class TagAdmin(ModelView, model=Tag):
    column_list = [Tag.description, Tag.fields]


class FileAdmin(ModelView, model=File):
    column_list = [File.id, File.path]


class SquadAdmin(ModelView, model=Squad):
    column_list = [Squad.name, Squad.members, Squad.files]


def register_admin(app: FastAPI):
    admin = Admin(app, engine, authentication_backend=AdminAuth(""))
    admin.add_view(UserAdmin)
    admin.add_view(FieldAdmin)
    admin.add_view(TagAdmin)
    admin.add_view(SquadAdmin)
    admin.add_view(FileAdmin)
