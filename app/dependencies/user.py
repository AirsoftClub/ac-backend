from fastapi import Request
from fastapi.responses import RedirectResponse

from app.schemas import User


def get_current_user(request: Request):
    user = request.session.get("user")
    if user:
        return User(**user)
    return RedirectResponse(request.url_for("login"))
