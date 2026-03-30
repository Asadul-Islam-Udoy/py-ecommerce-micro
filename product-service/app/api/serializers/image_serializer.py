from rest_framework import serializers
from api.models import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.CharField()
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "alt_text",
            "product",
            "is_active",
        ]
        
    # def validate_image(self, value):
    #     if value.size > 5 * 1024 * 1024:  # Limit to 5MB
    #         raise serializers.ValidationError("Image size should not exceed 5MB.")
    #     return value