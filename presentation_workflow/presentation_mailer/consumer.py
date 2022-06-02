from concurrent.futures import process
import json
import pika
import django
import os
import sys
from django.core.mail import send_mail


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()

while True:
    try:
        # ALL OF YOUR CODE THAT HANDLES READING FROM THE
        # QUEUES AND SENDING EMAILS
        parameters = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue="presentation_rejections")
        channel.queue_declare(queue="presentation_approvals")

        def process_approval(x, y, z, body):
            contact_info = json.loads(body)
            send_mail(
                "Your presentation has been accepted",
                f'{contact_info["presenter_name"]}, we\'re happy to tell you that your presentation {contact_info["title"]} has been approved',
                "admin@conference.go",
                [contact_info["presenter_email"]],
                fail_silently=False,
            )
            print("mail sent")

        def process_rejection(x, y, z, body):
            contact_info = json.loads(body)
            send_mail(
                "Your presentation has been denied",
                f'{contact_info["presenter_name"]}, we\'re sad to tell you that your presentation {contact_info["title"]} has been denied',
                "admin@conference.go",
                [contact_info["presenter_email"]],
                fail_silently=False,
            )
            print("mail sent")

        channel.basic_consume(
            queue="presentation_rejections",
            on_message_callback=process_rejection,
            auto_ack=True,
        )
        channel.basic_consume(
            queue="presentation_approvals",
            on_message_callback=process_approval,
            auto_ack=True,
        )
        channel.start_consuming()
    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)
