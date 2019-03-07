"""
Database schema using mongoengine Document-Object Mapper
"""

from mongoengine import Document
from mongoengine import StringField
from mongoengine import IntField


class Customer(Document):
    """
    Customer document definition
    """
    user_id = StringField(required=True, max_length=15)
    name = StringField(required=True, max_length=30)
    address = StringField(required=True, max_length=40)
    zip_code = IntField()
    phone_number = StringField(required=True, max_length=15)
    email = StringField(required=True, max_length=40)


class Product(Document):
    """
    Product document definition
    """
    product_id = StringField(required=True, max_length=15)
    description = StringField(required=True, max_length=30)
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
