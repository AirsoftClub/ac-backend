from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app.dependencies import get_client

router = APIRouter()


@router.get("/login")
async def login(
    request: Request,
    oauth: OAuth = Depends(get_client),
    next_url: str = "/",
):
    redirect_uri = str(request.url_for("callback"))
    request.session["next_url"] = next_url
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/logout")
async def logout(
    request: Request,
):
    request.session.pop("user")
    return RedirectResponse(request.url_for("home"))


@router.get("/google/callback")
async def callback(
    request: Request,
    oauth: OAuth = Depends(get_client),
):
    user = await oauth.google.authorize_access_token(request)
    user_info = user["userinfo"]
    request.session["user"] = {
        "email": user_info["email"],
        "name": f"{user_info['given_name']} {user_info['family_name']}",
        "image": user_info["picture"],
    }
    next_url = request.session.pop("next_url")
    return RedirectResponse(next_url)
