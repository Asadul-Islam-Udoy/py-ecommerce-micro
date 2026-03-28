from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers.payment_serializer import PaymentSerializer
from .services.payment_service import PaymentService


# Create your views here.
class CreatePaymentView(APIView):

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = PaymentService.create_payment(serializer.validated_data)

        return Response(result)