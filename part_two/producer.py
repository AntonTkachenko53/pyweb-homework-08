import pika
from model import Contact
from faker import Faker
from bson import ObjectId
from connect import connect


fake = Faker()


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_sender')

for i in range(20):
    model = Contact(fullname=fake.name(),
                    email=fake.email(),
                    phone=fake.phone_number(),
                    email_send=False)

    model.save()
    body = model.id.binary

    channel.basic_publish(exchange='', routing_key='email_sender', body=body)

connection.close()
