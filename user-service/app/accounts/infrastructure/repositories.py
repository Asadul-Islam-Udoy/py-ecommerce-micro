from .models import User,Role,Permission
from rest_framework.exceptions import ValidationError
from django.http import Http404
class RoleRepository:
    @staticmethod
    def get_role_by_name(name):
        return Role.objects.filter(name=name).first()
    
class PermissionRepository:
    @staticmethod
    def get_permission_by_code(code):
        return Permission.objects.filter(code=code).first()
    
    
class UserRepository:
    @staticmethod
    def create_user(email,password,role_name):
        if User.objects.filter(email=email).exists():
            raise ValueError("EMAIL_ALREADY_EXISTS")
        role = RoleRepository.get_role_by_name(role_name)
        user = User(email=email,password=password,role=role)
        user.set_password(password)
        user.save()
        return user
    
    def get_user_by_email(email):
        return User.objects.filter(email=email).first()
    
    
    def update_user(user_id, data):
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise Http404("User not found")

        allowed_fields = ['username']
        updated_fields = []

        for field in allowed_fields:
            if field in data:
                value = data[field]
                if isinstance(value, str):
                    value = value.strip()
                setattr(user, field, value)
                updated_fields.append(field)

        if not updated_fields:
            raise ValidationError("No valid fields to update")

        user.save(update_fields=updated_fields)
        return user
               
        