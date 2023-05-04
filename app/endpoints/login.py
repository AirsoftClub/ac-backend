from fastapi import APIRouter, Depends, Request
import os
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth

from app.dependencies.db import get_db
from app.models import SessionLocal


router = APIRouter()


def get_client() -> OAuth:
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID") or None
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET") or None
    if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
        raise BaseException("Missing google oauth secrets")

    # Set up oauth
    config_data = {
        "GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID,
        "GOOGLE_CLIENT_SECRET": GOOGLE_CLIENT_SECRET,
    }
    starlette_config = Config(environ=config_data)
    oauth = OAuth(starlette_config)
    oauth.register(
        name="google",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )
    return oauth


@router.get("/login")
async def login(request: Request, session: SessionLocal = Depends(get_db)):
    redirect_uri = str(request.url_for("callback"))
    oauth = get_client()
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def callback(request: Request, session: SessionLocal = Depends(get_db)):
    oauth = get_client()
    user_info = await oauth.google.authorize_access_token(request)
    return user_info
