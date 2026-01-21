from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from accounts.services.user_services import UserService
from .permissions import HasPermission
from accounts.domain.permissions import Permissions
from rest_framework.permissions import AllowAny
from django.template.context_processors import request
from accounts.api.serializers import LoginSerializer
from accounts.services.auth_services import AuthService
from accounts.api.serializers import RegisterSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        result = AuthService.login(serializer.validated_data)
        response =  Response(result,status=status.HTTP_200_OK)
        response.set_cookie(
            key="refresh_token",
            value=result["refresh"],
            httponly=True,
            secure=False,  # True if using HTTPS
            samesite="Lax",
            max_age=7*24*60*60  # 7 days
        )
        
        response.data["user"] = result["user"]
        
        return response
    
    
class UserProfileView(APIView):
    permission_classes = [HasPermission]
    required_permission = Permissions.USER_VIEW

    def get(self, request):
        return Response({"email": request.user.email})

class UserUpdateView(APIView):
    permission_classes = [HasPermission]
    required_permission = Permissions.USER_VIEW

    def put(self, request):
        if not request.user.has_permission(self.required_permission):
            return Response({"detail": "Forbidden"}, status=403)
        return Response({"message": "User updated"})
