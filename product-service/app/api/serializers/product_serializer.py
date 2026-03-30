from decimal import Decimal

from rest_framework import serializers
from api.models import Product,ProductVariant,ProductImage
from api.serializers.variant_serializer import ProductVariantSerializer
from api.serializers.image_serializer import ProductImageSerializer

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'brand', 'price', 'variants', 'images']
        
        
    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required.")
        return value
    
    def validate_price(self, value):
        if value in (None, ''):
            raise serializers.ValidationError("Price is required.")
        try:
            value = Decimal(value)
        except:
            raise serializers.ValidationError("Price must be a number.")
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value
    
    def validate(self,data):
        variants = data.get('variants')
        if not variants or len(variants) == 0:
            raise serializers.ValidationError("At least one variant is required.")
        
        sku_set = set()
        for variant in variants:
            sku = variant.get('sku')
            if sku in sku_set:
                raise serializers.ValidationError(f"Duplicate SKU found: {sku}")
            sku_set.add(sku)

        return data
    
    def create(self, validated_data):
        variants_data = validated_data.pop('variants', [])
        images_data = validated_data.pop('images', [])

        # Ensure price is Decimal
        validated_data['price'] = Decimal(validated_data['price'])

        # Create the product first
        product = Product.objects.create(**validated_data)

        # Bulk create variants
        variant_objs = [ProductVariant(product=product, **variant) for variant in variants_data]
        if variant_objs:
            ProductVariant.objects.bulk_create(variant_objs)

        # Bulk create images
        image_objs = [ProductImage(product=product, **image) for image in images_data]
        if image_objs:
            ProductImage.objects.bulk_create(image_objs)

        return product
