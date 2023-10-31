import pika  # Import the 'pika' library for RabbitMQ communication
import base64

def upload_image_to_queue(image_path):
    # Establish a connection to RabbitMQ
    url_params = pika.URLParameters('amqp://rabbit_mq?connection_attempts=10&retry_delay=10')

    # Establish a blocking connection to the RabbitMQ server
    connection = pika.BlockingConnection(url_params)

    channel = connection.channel()

    # Declare exchange and queue for image upload
    channel.exchange_declare(exchange='image_exchange', exchange_type='direct')
    channel.queue_declare(queue='image_queue')
    channel.queue_bind(exchange='image_exchange', queue='image_queue', routing_key='images')

    # Convert the image to base64 format
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Send the image to the queue
    channel.basic_publish(exchange='image_exchange', routing_key='images', body=image_data)

    print("Image successfully uploaded to the queue")
    connection.close()

image_path = 'img.jpg'
upload_image_to_queue(image_path)
