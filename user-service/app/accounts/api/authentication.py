import jwt
from django.conf import settings
from rest_framework import exceptions
from pathlib import Path
from rest_framework.authentication import BaseAuthentication
from accounts.infrastructure.models import User
KEYS_DIR = Path(settings.BASE_DIR)/'accounts'/'keys'
PRIVATE_KEY = (KEYS_DIR / "private.pem").read_text()
PUBLIC_KEY = (KEYS_DIR / "public.pem").read_text()

class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split()
        except ValueError:
            raise exceptions.AuthenticationFailed("Invalid Authorization header format")

        if prefix.lower() != "bearer":
            raise exceptions.AuthenticationFailed("Authorization header must start with Bearer")

        try:
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")

        try:
            user = User.objects.get(id=payload["sub"])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")

        return (user, None)