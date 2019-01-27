"""
Database models for HP Norton.
"""

from peewee import *


DATABASE = SqliteDatabase('hpnorton.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only


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

    customer_id = CharField(primary_key = True)
    name = CharField(max_length = 25, null=False)
    lastname = CharField(max_length = 25, null=False)
    home_address = CharField(max_length=40)
    phone_number = CharField(max_length=10)
    email = CharField(max_length=40)
    status = CharField(max_length=8, null=False)
    credit_limit = IntegerField()
