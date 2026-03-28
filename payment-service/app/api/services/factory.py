from .stripe_service import StripeService
from .paypal_service import PaypalService

class PaymentFactory:

    @staticmethod
    def get_service(method):
        if method == "stripe":
            return StripeService()
        elif method == "paypal":
            return PaypalService()
        else:
            raise Exception("Unsupported payment method")