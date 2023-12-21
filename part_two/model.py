from mongoengine import Document
from mongoengine.fields import StringField, BooleanField


class Contact(Document):
    fullname = StringField()
    email = StringField()
    phone = StringField()
    email_send = BooleanField(default=False)
