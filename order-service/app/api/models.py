from django.db import models
import uuid


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Order(BaseModel):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PROCESSING = "PROCESSING", "Processing"
        SHIPPED = "SHIPPED", "Shipped"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"

    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order_number = models.CharField(max_length=50, unique=True, db_index=True)

    user_id = models.UUIDField(db_index=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    currency = models.CharField(max_length=10, default="USD")

    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    notes = models.TextField(blank=True, null=True)

    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "orders"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.order_number}"


class OrderItem(BaseModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )

    product_id = models.UUIDField(db_index=True)

    product_name = models.CharField(max_length=255)

    product_sku = models.CharField(max_length=100, blank=True, null=True)

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(max_digits=12, decimal_places=2)

    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "order_items"
        indexes = [
            models.Index(fields=["product_id"]),
        ]

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"