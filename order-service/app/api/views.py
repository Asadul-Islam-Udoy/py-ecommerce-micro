from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers.order_serializer import (
    CreateOrderSerializer,
    OrderSerializer
)
from .services.order_service import OrderService
# Create your views here.
class OrderView(APIView):
    
    def get(self,request):
        
        filters = {
            "user_id": request.query_params.get("user_id"),
            "status": request.query_params.get("status"),
        }

        page = int(request.query_params.get("page", 1))
        limit = int(request.query_params.get("limit", 10))

        result = OrderService.get_orders(filters, page, limit)

        return Response({
            "data": OrderSerializer(result["data"], many=True).data,
            "meta": result["meta"]
        })
    
    def post(self,request):
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            order = OrderService.create_order(
                user_id=serializer.validated_data["user_id"],
                items=serializer.validated_data["items"]
                )
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    def patch(self, request, order_id=None):

        if not order_id:
            return Response(
                {"error": "Order ID required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get("status")
        payment_status = request.data.get("payment_status")

        if new_status:
            order.status = new_status

        if payment_status:
            order.payment_status = payment_status

        order.save(update_fields=["status", "payment_status"])

        return Response({
            "message": "Order updated successfully",
            "order": OrderSerializer(order).data
        })
 
        
class SingleOrderView(APIView):

    def get(self, request, order_id):

        order = OrderService.get_order_by_id(order_id)

        if not order:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_200_OK
        )