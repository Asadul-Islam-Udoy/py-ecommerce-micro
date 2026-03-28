import paypalrestsdk
from django.conf import settings

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET
})

class PaypalService:

    def create_payment(self, transaction):
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {
                    "total": str(transaction.amount),
                    "currency": transaction.currency
                }
            }]
        })

        payment.create()
        return {"id": payment.id}

    def verify_payment(self, data):
        return True

    def refund_payment(self, transaction):
        pass