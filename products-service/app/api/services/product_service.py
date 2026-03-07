from api.models import Product, ProductVariant, ProductImage
from django.db.models import Prefetch,Q
from django.core.paginator import Paginator
from django.db import transaction

class ProductService:
    @staticmethod
    def create_product(self, product_data,images_data):
        # Logic to create a new product using the provided data
        variants_data = product_data.pop('variants',[])
        product = Product.objects.create(**product_data)
        
        variants_objs = [ProductVariant(product=product, **v) for v in variants_data]
        
        if variants_objs:
            ProductVariant.objects.bulk_create(variants_objs)
            
        images_objs = []
        if images_data:
            for img in images_data:
                images_objs.append(ProductImage(product=product, **img))
            if images_objs:
                ProductImage.objects.bulk_create(images_objs)
        return product  
    
       
    @staticmethod
    def get_products(page=1,per_page=10,brand=None, min_price=None, max_price=None, search=None, order_by='-id'):
        queryset =  (
            Product.objects.only('id','title','description','brand','price').prefetch_related(Prefetch('variants'), Prefetch('images'))
        )
        if brand:
            queryset = queryset.filter(brand__iexact=brand)
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        queryset = queryset.order_by(order_by)
        paginator = Paginator(queryset, per_page) 
        page_obj = paginator.get_page(page)
        
        return {
            'products': page_obj.object_list,
            'total_pages': paginator.num_pages,
            'current_page': page_obj.number,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous()
        }
    
    
    @staticmethod
    def get_product_by_id(product_id):
        try:
            return Product.objects.prefetch_related('variants','images').get(id=product_id)
        except Product.DoesNotExist:
            return None
        
    @staticmethod
    @transaction.atomic
    def update_product(product_id,product_data,images_data,variant_data):
        product = Product.objects.get(id=product_id)
        
        for key,value in product_data.items():
            setattr(product,key,value)
        product.save()
        
        if images_data is not None:
            existing_imges = {img.id:img for img in product.images.all() if img.id}
            images_to_create = []
            images_to_update = []
            
            for img in images_data:
                img_id = img.get('id')
                if img_id and img_id in existing_imges:
                    for key,value in img.items():
                        if key !='id':
                            setattr(existing_imges[img_id],key,value)
                    images_to_update.append(existing_imges[img_id])
                else:
                    images_to_create.append(ProductImage(product=product, **img))
            if images_to_update:
                ProductImage.objects.bulk_update(images_to_update,fields=[k for k in images_data[0].keys() if k != 'id'])
            else:    
                ProductImage.objects.bulk_create(images_to_create)   
        if  variant_data is not None:
            existing_variants = {v.id:v for v in product.variants.all() if v.id}
            variants_to_create = []  
            variants_to_update = [] 
            
            for var in variant_data:
                var_id = var.get('id')
                
                if var_id and var_id in existing_variants:
                    for key,value in var.items():
                        if key != 'id':
                            setattr(existing_variants[var_id],key,value)  
                    variants_to_update.append(existing_variants[var_id])
                else:
                    variants_to_create.append(ProductVariant(product=product, **var))
            if variants_to_update:
                ProductVariant.objects.bulk_update(variants_to_update,fields=[k for k in variant_data[0].keys() if k != 'id'])
            if variants_to_create:
                ProductVariant.objects.bulk_create(variants_to_create)
                
                
            # updated_var_ids = [v.get('id') for v in variant_data if v.get('id')]
            # product.variants.exclude(id__in=updated_var_ids).delete()
        
        return product
            
    @staticmethod
    def delete_product(product_id):
        product = Product.objects.get(id=product_id)
        product.delete()
        return True