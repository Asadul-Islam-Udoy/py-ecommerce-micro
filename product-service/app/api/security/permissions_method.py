from rest_framework.permissions import BasePermission

class MethodPermission(BasePermission):
    """
    Method-level permission mapping:
    GET → product-get
    POST → product-create
    PUT → product-update
    DELETE → product-delete
    """
    def has_permission(self, request, view):
        method_perms = getattr(view, "method_permissions", {})
        required_permission = method_perms.get(request.method)
        if not required_permission:
            # No permission defined → deny
            return False

        user_permissions = getattr(request, "permissions", [])
        return required_permission in user_permissions
    
    
    
    
    # permission_classes = [MethodPermission]

    # method_permissions = {
    #     "GET": "product-get",
    #     "POST": "product-create",
    #     "PUT": "product-update",
    #     "DELETE": "product-delete",
    # }
    
    
    
#   PRODUCT_METHOD_PERMISSIONS = {
#     "GET": "product-get",
#     "POST": "product-create",
#     "PUT": "product-update",
#     "DELETE": "product-delete",
# }

# ORDER_METHOD_PERMISSIONS = {
#     "GET": "order-get",
#     "POST": "order-create",
#     "PUT": "order-update",
#     "DELETE": "order-delete",
# }

# permission_classes = [MethodPermission]
#  method_permissions = PRODUCT_METHOD_PERMISSIONS