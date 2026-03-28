
from django.urls import path
from .views import CreatePaymentView
from .webhook.payment_webhook import  WebhookView
urlpatterns = [
    path('create/', CreatePaymentView.as_view(), name='payment-create'),
    path("webhook/<str:provider>/", WebhookView.as_view(), name="payment-webhook"),
    # path("status/<str:order_id>/", TransactionStatusView.as_view(), name="transaction-status"),
]