from .models import User,Role,Permission

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