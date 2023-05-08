from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app.dependencies import get_client, get_repository
from app.repositories import UserRepository
from app.schemas import UserSchema

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


@router.get("/google/callback")
async def callback(
    request: Request,
    oauth: OAuth = Depends(get_client),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
):
    # Retrieve the user's profile information
    user_profile = await oauth.google.authorize_access_token(request)
    user_info = user_profile["userinfo"]
    # Map user profile data to UserSchema
    user_data = UserSchema(
        first_name=user_info["given_name"],
        last_name=user_info["family_name"],
        email=user_info["email"],
        image=user_info["picture"],
    )
    # Create or update the user in the database
    user_repo.create_or_update(user_data)
    # Store the user data in the session
    request.session["user"] = user_data.dict()
    next_url = request.session.pop("next_url")
    # Redirect the user to the next URL
    return RedirectResponse(next_url)


@router.get("/logout")
async def logout(
    request: Request,
):
    request.session.pop("user")
    return RedirectResponse(request.url_for("home"))
