from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from app.core.settings import settings


def get_client() -> OAuth:
    starlette_config = Config(
        environ={
            "GOOGLE_CLIENT_ID": settings.GOOGLE.CLIENT_ID,
            "GOOGLE_CLIENT_SECRET": settings.GOOGLE.CLIENT_SECRET,
        }
    )
    oauth = OAuth(starlette_config)
    oauth.register(
        name="google",
        server_metadata_url=settings.GOOGLE.SERVER_METADATA_URL,
        client_kwargs={"scope": "openid email profile"},
    )
    return oauth
