from accounts.infrastructure.repositories import UserRepository
from accounts.api.jwt import generate_tokens
from rest_framework.exceptions import ValidationError
class UserService:
    @staticmethod
    def register(data):
        try:
            user = UserRepository.create_user(
                email=data["email"],
                password=data["password"],
                role_name=data.get("role", "user"),
            )
        except ValueError as e:
            if str(e) == "EMAIL_ALREADY_EXISTS":
                raise ValidationError({"email": "User with this email already exists"})

        access, refresh = generate_tokens(user)
        
        return {
            "user": {
                "id": user.id,
                "email": user.email,
            },
            "access": access,
            "refresh": refresh,
        }
