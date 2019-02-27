from mongoengine import Document
from mongoengine import StringField
from mongoengine import IntField
from mongoengine import ReferenceField


"""
class Author(Document):
    name = StringField()

class Post(Document):
    author = ReferenceField(Author)

Post.objects.first().author.name
"""


class Customer(Document):
    user_id = StringField(required=True, max_length=15)
    name = StringField(required=True, max_length=30)
    address = StringField(required=True, max_length=40)
    phone = StringField(required=True, max_length=15)
    email = StringField(required=True, max_length=40)


class Product(Document):
    prod_id = StringField(required=True, max_length=15)
    description = StringField(required=True, max_length=30)
    prod_type = StringField(required=True, max_length=15)
    quantity = IntField()


class Rental(Document):
    prod_id = ReferenceField(Product)
    user_id = ReferenceField(Customer)

