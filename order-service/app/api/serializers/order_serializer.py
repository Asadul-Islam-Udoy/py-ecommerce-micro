
from rest_framework import serializers
from api.models import Order, OrderItem

class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=255)
    product_sku = serializers.CharField(max_length=100, allow_blank=True, required=False)
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    quantity = serializers.IntegerField()
    
    
class CreateOrderSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    items = OrderItemInputSerializer(many=True)
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")

        for item in value:
            if item["quantity"] <= 0:
                raise serializers.ValidationError("Quantity must be greater than 0.")

            if item["price"] <= 0:
                raise serializers.ValidationError("Price must be greater than 0.")

        return value


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"









