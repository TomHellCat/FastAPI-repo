from mongoengine import Document, StringField, IntField

class Inventory(Document):
    item = StringField(max_length=50)
    color = StringField(max_length=10)
    qty = IntField()

class User(Document):
    username = StringField()
    password = StringField()