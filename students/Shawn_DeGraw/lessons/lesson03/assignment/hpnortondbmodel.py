"""
Database models for HP Norton.
"""

from peewee import *
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('hpnorton.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only


class BaseModel(Model):
    """ Base model class to establish database connection """

    class Meta:
        database = database


class Customer(BaseModel):
    """
        This class defines Customer. Contains all customer information
        for HP Norton.

        customerid, name, lastname, homeaddress, 
        phonenumber, email, status, creditlimit
    """

    customer_id = IntegerField(primary_key = True, max_length = 5)
    name = CharField(max_length = 25, null=False)
    lastname = CharField(max_length = 25, null=False)
    home_address = CharField(max_length=40, null)
    phone_number = CharField(max_length=12)
    email = CharField(max_length=40)
    status = BooleanField(null=False)
    credit_limit = IntegerField(max_length=5)
