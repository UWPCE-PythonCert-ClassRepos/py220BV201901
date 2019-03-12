"""
Database schema using mongoengine Document-Object Mapper
"""

from mongoengine import Document
from mongoengine import StringField
from mongoengine import IntField
from mongoengine import BooleanField


class Customer(Document):
    """
    Customer document definition
    """
    user_id = StringField(required=True, max_length=15)
    name = StringField(required=True, max_length=15)
    last_name = StringField(required=True, max_length=15)
    address = StringField(required=True, max_length=40)
    phone_number = StringField(required=True, max_length=30)
    email = StringField(required=True, max_length=40)
    status = BooleanField(required=True)
    credit_limit = IntField(required=True)


class Product(Document):
    """
    Product document definition
    """
    product_id = StringField(required=True, max_length=15)
    description = StringField(required=True, max_length=45)
    product_type = StringField(required=True, max_length=15)
    quantity_available = IntField()


class Rental(Document):
    """
    Rental document definition
    """
    product_id = StringField(required=True, max_length=15)
    user_id = StringField(required=True, max_length=15)


def util_drop_all():
    """ utility funciton to drop all collections """
    Customer.drop_collection()
    Product.drop_collection()
    Rental.drop_collection()
