import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:

    def create_payment(self, transaction):
        intent = stripe.PaymentIntent.create(
            amount=int(transaction.amount * 100),
            currency=transaction.currency,
        )
        return {
            "id": intent.id,
            "client_secret": intent.client_secret
        }

    def verify_payment(self, data):
        intent = stripe.PaymentIntent.retrieve(data["id"])
        return intent.status == "succeeded"

    def refund_payment(self, transaction):
        stripe.Refund.create(payment_intent=transaction.external_id)