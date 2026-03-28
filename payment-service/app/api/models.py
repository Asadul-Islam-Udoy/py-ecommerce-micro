from django.db import models
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Transaction(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending"
        SUCCESS = "success"
        FAILED = "failed"
        CANCELLED = "cancelled"

    class PaymentMethod(models.TextChoices):
        STRIPE = "stripe"
        PAYPAL = "paypal"
        SSL = "sslcommerz"

    user_id = models.UUIDField()
    order_id = models.CharField(max_length=255, db_index=True)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )

    external_id = models.CharField(max_length=255, null=True, blank=True)
    client_secret = models.TextField(null=True, blank=True)

    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.order_id} - {self.status}"


class PaymentEvent(BaseModel):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="events"
    )

    event_type = models.CharField(max_length=100)
    provider = models.CharField(max_length=50)  # stripe / paypal

    raw_data = models.JSONField()

    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.event_type} - {self.provider}"


class IdempotencyKey(BaseModel):
    key = models.CharField(max_length=255, unique=True)

    request_hash = models.CharField(max_length=255)
    response = models.JSONField()

    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return self.key