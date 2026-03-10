from django.http import JsonResponse
from .jwt_decoder import decode_token


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        auth_header = request.headers.get("Authorization")

        # Check if header is missing
        if not auth_header:
            return JsonResponse({"error": "Authorization header missing"}, status=401)

        parts = auth_header.split(" ")

        # Validate header format
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return JsonResponse({"error": "Invalid Authorization header"}, status=401)

        token = parts[1]

        try:
            payload = decode_token(token)
            request.user_id = payload.get("user_id")
            request.permissions = payload.get("permissions", [])
        except Exception as e:
            return JsonResponse({"error": "Invalid token", "detail": str(e)}, status=401)

        return self.get_response(request)