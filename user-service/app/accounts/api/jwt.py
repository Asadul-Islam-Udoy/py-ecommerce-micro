import jwt,datetime
from django.conf import settings
from accounts.infrastructure.models import User
from pathlib import Path
BASE_DIR = settings.BASE_DIR

KEYS_DIR = Path(BASE_DIR) / settings.JWT["PRIVATE_KEY_PATH"].rsplit("/", 1)[0]

PRIVATE_KEY = (BASE_DIR / settings.JWT["PRIVATE_KEY_PATH"]).read_text()
PUBLIC_KEY = (BASE_DIR / settings.JWT["PUBLIC_KEY_PATH"]).read_text()

def generate_tokens(user:User):
    access_payload = {
        "sub":str(user.id),
        "role": user.role.name if user.role else None,
        "permissions": [p.code for p in user.role.permissions.all()] if user.role else [],
        "is_superuser": user.is_superuser,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
    }
    access = jwt.encode(access_payload, PRIVATE_KEY, algorithm="RS256")
    
    refresh_payload = {
        "sub": str(user.id),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }
    refresh = jwt.encode(refresh_payload, PRIVATE_KEY, algorithm="RS256")
    
    return access, refresh


    