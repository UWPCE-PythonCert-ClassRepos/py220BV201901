# Student: Bradnon Nguyen
# Class:   Advance Python 220 - Jan2019
# Lesson03 - customer_db_model.py
"""
This will create a customer model and database that can be used at HP Norton with the 
following data:
Customer ID. Name. Lastname. Home address.
Phone number. Email address.
Status (active or inactive customer).  Credit limit.
"""
from peewee import *

DB = SqliteDatabase('customers.db')

class BaseModel(Model):
    """ base Model peewee Object Relational Mapping - ORM """
    class Meta:
        # database = SqliteDatabase('HPCustomer.db') # Why not here?
        database = DB


class Customer(BaseModel):
    """
        This class defines a customer model in HP HP Norton, which maintains details of
        someone to support: Saleperson, Accountant, Manager.
        Fields: customer_id, name, last_name, home_address, phone_number, email
        status, credit_limit.
    """

# Customer ID, Name, Lastname, Home address, Phone number, Email address, Status (active or inactive customer), Credit limit.

    customer_id = CharField(primary_key=True, max_length=20)
    name = CharField(null=True)
    lastname = CharField(null=True)
    home_address = CharField(null=True, max_length=255)
    phone_number = CharField(null=True, max_length=20)
    email = CharField(null=True, max_length=254)  # RFC xxyy
    status = CharField(null=True, max_length=8)
    credit_limit = CharField(null=True)
    # These will fail Andy's tests
    #status = CharField(null=True, constraints=[Check("status == 'active' or status == 'inactive'")])
    #credit_limit = IntegerField(null=True, constraints=[Check('credit_limit <= 0')])

