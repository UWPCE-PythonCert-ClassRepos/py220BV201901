'''
Yushu Song
Assignment04
'''

from peewee import *

DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')

class Customer(Model):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    customer_id = CharField(primary_key=True)
    first_name = CharField(max_length=40)
    last_name = CharField(max_length=40)
    home_address = TextField()
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=40)
    status = BooleanField()
    credit_limit = DecimalField(max_digits=2)

    class Meta:
        '''
        Meta class
        '''
        database = DATABASE
