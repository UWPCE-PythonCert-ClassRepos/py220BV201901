"""
Database model for HP Norton to store customer information,
custommer credit information,
monthly active customer informaiont
"""

import logging
from peewee import *

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

database = SqliteDatabase('customer.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    class Meta:
        database = database

class Customer(BaseModel):
    logging.info("Customer class, coresponses to customer table in database")
    """
    This class defines customer, which includes information of customer_id,
    name, lastname, home_address, phone_number, email_address, status, credit_limit.
    """

    customer_id = CharField(primary_key = True, max_length=30)
    name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=50)
    phone_number = CharField(max_length=12)
    email_address = TextField()
    status = BooleanField(help_text='True means active, False means in-active', null=False)
    credit_limit = DecimalField(decimal_places=2)
