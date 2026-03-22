from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
# ----------------------------
# Permission & Role
# ----------------------------
class Permission(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.code


class Role(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission, related_name="roles", blank=True)

    def __str__(self):
        return self.name


# ----------------------------
# User Manager
# ----------------------------
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        if password:
            user.set_password(password)
        user.set_username()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        return self.create_user(email, password, **extra_fields)


# ----------------------------
# User Model
# ----------------------------
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for admin
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"      # Login with email
    REQUIRED_FIELDS = ["username"]  # Asked during createsuperuser

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def has_permission(self, perm_code):
        if self.is_superuser:
            return True
        if not self.role:
            return False
        return perm_code in [p.code for p in self.role.permissions.all()]

    def set_username(self):
        if not self.username:
            self.username = self.email.split("@")[0]

    def __str__(self):
        return self.email
