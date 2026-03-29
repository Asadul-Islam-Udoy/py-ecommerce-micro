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
from accounts.api.serializers import UserUpdateSerializer
from django.http import Http404
from rest_framework.exceptions import ValidationError

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
    

class UpdateView(APIView):
    permission_classes = [HasPermission]
    required_permission = Permissions.USER_VIEW

    def patch(self, request, user_id=None):
        target_user_id = user_id or request.user.id

        # Permission check (admin vs self)
        if target_user_id != request.user.id:
            if not request.user.has_permission(self.required_permission):
                return Response(
                    {"detail": "Forbidden"},
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = UserService.update_user(
                target_user_id,
                serializer.validated_data
            )

        except ValidationError as e:
            # Business / field validation errors
            return Response(
                {"errors": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Http404:
            # User not found
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception:
            # Unexpected error (log this in production)
            return Response(
                {"detail": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
                {
                    "message": "User updated successfully",
                    "user": {
                        "id": result.id,
                        "username": result.username,
                        "email": result.email,
                    }
                },
                status=status.HTTP_200_OK
            )
