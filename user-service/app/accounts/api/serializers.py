from django.forms import ValidationError
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
    
    
    
class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(required=False,allow_blank=True, min_length=3,
        max_length=50)
    
    def validate(self,attrs):
        if not attrs:
            raise serializers.ValidationError(
                "At least one field must be provided."
            )
        if  attrs.get('username'):
            value =attrs.get('username').strip()
            if not value.replace("_","").isalnum():
                raise serializers.ValidationError(
                "Username may contain letters, numbers, and underscores only."
            )
        return attrs