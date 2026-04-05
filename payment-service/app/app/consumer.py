import pika
import json
import time

def process_payment(order_data):
    print(" Processing payment...")
    time.sleep(2)  # simulate delay

    # fake success
    return {
        "order_id": order_data["order_id"],
        "status": "success"
    }


def callback(ch, method, properties, body):
    data = json.loads(body)

    if data["event"] == "order_created":
        order_data = data["data"]

        result = process_payment(order_data)

        print(" Payment Done:", result)

        # OPTIONAL: send back event to order service
        publish_payment_event(result)


def publish_payment_event(data):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq')
    )
    channel = connection.channel()

    channel.exchange_declare(exchange='events', exchange_type='fanout')

    channel.basic_publish(
        exchange='events',
        routing_key='',
        body=json.dumps({
            "event": "payment_success",
            "data": data
        })
    )

    connection.close()


def start_consumer():
    while True:
        try:
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

            print(" Payment service listening...")
            channel.start_consuming()

        except Exception as e:
            print(" Error:", e)
            print("Retrying in 5 seconds...")
            time.sleep(5)