from rest_framework.views import APIView
from api.models import Transaction
from api.services.factory import PaymentFactory
from rest_framework.response import Response

class WebhookView(APIView):
    def post(self, request, provider):
        service = PaymentFactory.get_service(provider)
        verified = service.verify_payment(request.data)

        if verified:
            transaction = Transaction.objects.get(external_id=request.data["id"])
            transaction.status = Transaction.Status.SUCCESS
            transaction.save()
            transaction.events.create(
                event_type="payment_success",
                provider=provider,
                raw_data=request.data
            )
        return Response({"status": "ok"})