"""
Database models for HP Norton.
"""

from peewee import *


DATABASE = SqliteDatabase('customers.db')


class BaseModel(Model):
    """ Base model class to establish database connection """

    class Meta:
        database = DATABASE


class Customer(BaseModel):
    """
        This class defines Customer. Contains all customer information
        for HP Norton.

        customerid, name, lastname, homeaddress, 
        phonenumber, email, status, creditlimit
    """

    customer_id = CharField(primary_key = True, max_length=10)
    name = CharField(max_length = 25, null=True)
    lastname = CharField(max_length = 25, null=True)
    home_address = CharField(max_length=40, null=True)
    phone_number = CharField(max_length=20, null=True)
    email = CharField(max_length=40, null=True)
    status = CharField(max_length=8, null=True)
    credit_limit = IntegerField(null=True)
