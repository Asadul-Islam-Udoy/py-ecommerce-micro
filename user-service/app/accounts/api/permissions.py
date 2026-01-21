
from rest_framework.permissions import BasePermission
class HasPermission(BasePermission):
    required_permission = None
    
    def has_permisson(self,request,view):
        if not getattr(view, "required_permission", None):
            return True
        
        user = request.user
        if not user or not getattr(user, "is_authenticated", False):
            return False
        return user.has_permission(self.required_permission)