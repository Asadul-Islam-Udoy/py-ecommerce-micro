from rest_framework import serializers
from api.models import Product
from api.serializers.variant_serializer import ProductVariantSerializer
from api.serializers.image_serializer import ProductImageSerializer

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'brand', 'price', 'variants', 'images']
        
        
    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required.")
        return value
    
    def validate(self,data):
        variants = data.get('variants')
        if not variants:
            raise serializers.ValidationError("At least one variant is required.")
        
        sku_set = set()
        for variant in variants:
            sku = variant.get('sku')
            if sku in sku_set:
                raise serializers.ValidationError(f"Duplicate SKU found: {sku}")
            sku_set.add(sku)

        return data