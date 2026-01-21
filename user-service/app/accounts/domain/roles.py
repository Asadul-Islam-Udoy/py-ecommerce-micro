from .permissions import Permissions

ROLE_PERMISSION_MAP = {
    "admin": {Permissions.USER_VIEW, Permissions.USER_UPDATE, Permissions.USER_VIEW_ALL},
    "user": {Permissions.USER_VIEW},
}
