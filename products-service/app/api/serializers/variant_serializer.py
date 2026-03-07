from rest_framework import serializers
from api.models import ProductVariant


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'variant_name', 'sku', 'stock_quantity', 'color', 'size', 'price']
        
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be a greater then zero!.")
        return value 
    
    def validate_stock_quantity(self, value):  
        if value < 0:
            raise serializers.ValidationError("Stock quantity must be a greater then zero!.")
        return value