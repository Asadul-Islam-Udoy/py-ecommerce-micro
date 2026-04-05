import pika
import json
from api.models import Order

def callback(ch, method, properties, body):
    data = json.loads(body)

    if data["event"] == "payment_success":
        order_id = data["data"]["order_id"]

        try:
            order = Order.objects.get(id=order_id)
            order.payment_status = "paid"
            order.status = "confirmed"
            order.save()

            print(f"✅ Order {order_id} updated after payment")

        except Order.DoesNotExist:
            print("❌ Order not found")


def start_consumer():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq')
    )

    channel = connection.channel()
    channel.exchange_declare(exchange='events', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='events', queue=queue_name)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    print("🎧 Order service listening...")
    channel.start_consuming()