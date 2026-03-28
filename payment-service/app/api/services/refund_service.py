
from api.models import Transaction
from api.services.factory import PaymentFactory
class RefundService:

    @staticmethod
    def refund(transaction_id):
        transaction = Transaction.objects.get(id=transaction_id)

        service = PaymentFactory.get_service(transaction.payment_method)
        service.refund_payment(transaction)

        transaction.status = "refunded"
        transaction.save()