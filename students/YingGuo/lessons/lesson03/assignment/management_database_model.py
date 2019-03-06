"""
Creat database for HP Norton to store customer information,
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
    This class defines customer, which includes information of Customer ID.
    Name. Lastname. Home address. Phone number. Email address. Credit limit.
    """

    customer_id = CharField(primary_key = True, max_length=30)
    customer_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=50)
    phone_number = CharField(max_length=12)
    email = TextField()
    credit_limit = DecimalField(decimal_places=2)

class Sale(BaseModel):
    """
    keep track of montly sales, if a customer has sales in this month,
    the status of this customer would be seen as active customer.
    """
    logging.info("Sale class, keep track of monthly sale")
    order_number = CharField(primary_key=True, max_length=5)
    order_date = DateField(formats='YYYY-MM-DD')
    status = BooleanField(help_text='True means active, False means in-active', null=False)
    customer_id = ForeignKeyField(Customer, related_name='was filled by', null=False)
