import pika
import json

def publish_event(event, data):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq')
    )
    channel = connection.channel()

    channel.exchange_declare(exchange='events', exchange_type='fanout')

    channel.basic_publish(
        exchange='events',
        routing_key='',
        body=json.dumps({
            "event": event,
            "data": data
        })
    )

    connection.close()