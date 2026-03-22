from rest_framework.exceptions import AuthenticationFailed
from accounts.repositories.user_repository import UserRepository
from accounts.api.jwt import generate_tokens

class AuthService:
    @staticmethod
    def login(validat_data):
        email = validat_data['email']
        password = validat_data['password']
        
        user = UserRepository.get_user_by_email(email=email)
        
        if not user :
            raise AuthenticationFailed('Invalid email')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password')
        
        if not user.is_active:
            raise AuthenticationFailed('User is not Active')
        access, refresh = generate_tokens(user) 
        
        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role.name if user.role else None,
            },
            "access": access,
            "refresh": refresh,
        }     