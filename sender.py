import pika


def send_to_fast_api(data):
    parameters = pika.URLParameters('amqp://admin:admin@rabbit:5672/')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    channel.basic_publish(
        exchange='',
        routing_key='hello',
        body=data
    )
    print(" [x] Sent 'Sending...'")
    connection.close()
