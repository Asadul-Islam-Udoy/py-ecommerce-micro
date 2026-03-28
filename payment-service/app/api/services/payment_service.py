from api.models import Transaction
from api.services.factory import PaymentFactory

class PaymentService:

    @staticmethod
    def create_payment(data):
        transaction = Transaction.objects.create(
            user_id=data["user_id"],
            order_id=data["order_id"],
            amount=data["amount"],
            currency="USD",
            payment_method=data["method"],
            status="pending"
        )

        service = PaymentFactory.get_service(data["method"])
        response = service.create_payment(transaction)

        transaction.external_id = response.get("id")
        transaction.client_secret = response.get("client_secret")
        transaction.status = "initiated"
        transaction.save()

        return response