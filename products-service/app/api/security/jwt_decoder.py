import jwt
from django.conf import settings
from pathlib import Path

PUBLIC_KEY_PATH = Path(settings.BASE_DIR) / "api" / "keys" / "public.pem"

with open(PUBLIC_KEY_PATH, "r") as f:
    PUBLIC_KEY = f.read()


def decode_token(token):
    payload = jwt.decode(
        token,
        PUBLIC_KEY,
        algorithms=["RS256"]
    )
    return payload