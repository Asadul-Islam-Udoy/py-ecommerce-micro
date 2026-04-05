from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from api.serializers.product_serializer import ProductSerializer
from api.serializers.variant_serializer import ProductVariantSerializer
from api.serializers.image_serializer import ProductImageSerializer
from api.services.product_service import ProductService

from api.security.permissions import (
    HasProductCreatePermission,
    HasProductUpdatePermission,
    HasProductGetPermission,
    HasProductDeletePermission
)
class ProductCreateView(APIView):
    permission_classes = [HasProductCreatePermission]
    def get(self, request):
        products = cache.get("products")
        if not products:
            products_qs = ProductService.get_all_products()
            products = ProductSerializer(products_qs, many=True).data
            cache.set("products", products, timeout=300)
        return Response(products, status=status.HTTP_200_OK)
   
    def post(self, request):
       
       images = request.FILES.getlist('images')
       variants = request.data.get('variants')
       serializer = ProductSerializer(data=request.data)
       if serializer.is_valid():
           product =  product = serializer.save()
           cache.delete("products")
           return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   
class ProductDetailView(APIView):
    permission_classes = [HasProductGetPermission]
    def get(self,request,pk):
        cache_key = f"product_{pk}"
        product_data = cache.get(cache_key)
        if not product_data:
            product = ProductService.get_product_by_id(pk)
            if not product:
                return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
            product_data = ProductSerializer(product).data
            cache.set(cache_key, product_data, timeout=300)
        return Response(product_data, status=status.HTTP_200_OK)
    
    
    def put(self,request,pk):
        images = request.FILES.getlist('images')
        variants = request.data.get('variants')
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = ProductService.update_product(pk,serializer.validated_data,images,variants)
            if not product:
                return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
            cache.delete("products")
            cache.delete(f"product_{pk}")
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        success = ProductService.delete_product(pk)
        if success:
            cache.delete("products")
            cache.delete(f"product_{pk}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)