from django.db import models

# Product model section
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    brand = models.CharField(max_length=255, blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'
        
    def __str__(self):
        return self.title

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    variant_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, unique=True)
    stock_quantity = models.IntegerField(default=0)
    color = models.CharField(max_length=50, blank=True,null=True)
    size = models.CharField(max_length=50, blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'product_variants'
        
    def __str__(self):
        return f"{self.product.title} - {self.variant_name}"
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/') 
    alt_text = models.CharField(max_length=255, blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'product_images'
        
    def __str__(self):
            return f"Image for {self.product.title}"