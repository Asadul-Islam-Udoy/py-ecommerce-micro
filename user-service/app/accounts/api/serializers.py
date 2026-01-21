from rest_framework  import serializers
from accounts.services.user_services import UserService

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(default='user')

    def create(self, validated_data):
        return UserService.register(
            validated_data
        )
        
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)