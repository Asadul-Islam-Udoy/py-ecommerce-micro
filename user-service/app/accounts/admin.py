from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .infrastructure.models import User, Role, Permission
from django.contrib.admin import AdminSite
# ----------------------------
# Permission Admin
# ----------------------------

class MyAdminSite(AdminSite):
    site_header = "Master E-commerce Admin"
    site_title = "Master E-commerce Portal"
    index_title = "Dashboard"

# create an instance
custom_admin_site = MyAdminSite(name="myadmin")



@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("code", "description")
    search_fields = ("code", "description")


# ----------------------------
# Role Admin
# ----------------------------
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    filter_horizontal = ("permissions",)  # allows easy ManyToMany editing


# ----------------------------
# User Admin
# ----------------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "role", "is_staff", "is_superuser", "is_active")
    list_filter = ("is_superuser", "is_staff", "is_active", "role")
    search_fields = ("email", "username")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Permissions", {"fields": ("role", "is_staff", "is_superuser", "is_active", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "role", "is_staff", "is_superuser", "is_active"),
        }),
    )
# register with custom admin site
custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Role, RoleAdmin)
custom_admin_site.register(Permission, PermissionAdmin)