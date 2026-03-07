from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers.product_serializer import ProductSerializer
from api.serializers.variant_serializer import ProductVariantSerializer
from api.serializers.image_serializer import ProductImageSerializer
from api.services.product_service import ProductService

class ProductCreateView(APIView):
    def get(self, request):
        products = ProductService.get_all_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
       images = request.FILES.getlist('images')
       variants = request.data.get('variants')
       serializer = ProductSerializer(data=request.data)
       if serializer.is_valid():
           product = ProductService.create_product(serializer.validated_data,images,variants)
           return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   
class ProductDetailView(APIView):
    def get(self,request,pk):
        product = ProductService.get_product_by_id(pk)
        if product:
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
    
    
    def put(self,request,pk):
        images = request.FILES.getlist('images')
        variants = request.data.get('variants')
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = ProductService.update_product(pk,serializer.validated_data,images,variants)
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        success = ProductService.delete_product(pk)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)