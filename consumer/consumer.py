# Import the 'pika' library for RabbitMQ communication.
import pika
import time

from PIL import Image
from io import BytesIO
import base64

def callback(ch, method, properties, body):
    try:
        # Decode the image from base64 to binary format
        image_data = base64.b64decode(body)

        # Convert the binary image data to an image object
        image = Image.open(BytesIO(image_data))

        # Resize the image (e.g., to 50x50 pixels)
        resized_image = image.resize((500, 500))

        # Save the resized image locally
        resized_image.save('resized_image.jpg')

        print("Image successfully resized and saved as 'resized_image.jpg'")
    except Exception as e:
        print(f"Error processing the image: {e}")

def consume_image_from_queue():
    # Establish a connection to RabbitMQ
    url_params = pika.URLParameters('amqp://rabbit_mq?connection_attempts=10&retry_delay=10')

    connection = pika.BlockingConnection(url_params)
    channel = connection.channel()

    # Declare the queue for receiving images
    channel.queue_declare(queue='image_queue')

    # Set the callback function for image processing
    channel.basic_consume(queue='image_queue', on_message_callback=callback, auto_ack=True)

    print("Waiting for an image from the queue...")
    channel.start_consuming()

consume_image_from_queue()
