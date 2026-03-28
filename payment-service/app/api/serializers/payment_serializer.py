from rest_framework import serializers
class PaymentSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    order_id = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    method = serializers.CharField()