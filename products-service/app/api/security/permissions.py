from rest_framework.permissions import BasePermission

class HasProductCreatePermission(BasePermission):
    def has_permission(self, request, view):
        return "product-create" in getattr(request, "permissions", [])

class HasProductUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        return "product-update" in getattr(request, "permissions", [])

class HasProductGetPermission(BasePermission):
    def has_permission(self, request, view):
        return "product-get" in getattr(request, "permissions", [])

class HasProductDeletePermission(BasePermission):
    def has_permission(self, request, view):
        return "product-delete" in getattr(request, "permissions", [])