'''
Database schema definition for customers database 'customers.db'
'''

from peewee import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Defining the data with schema definition')
logger.info('Naming and connecting to an sqlite database\n')

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

logger.info('Enabling PeeWee ORM...\n')

class BaseModel(Model):
    '''Enable PeeWee ORM'''

    class Meta:
        database = database


class Customers(BaseModel):
    '''This class defines Customers table data'''

    logger.info('Specify fields in model, their lengths, and if mandatory')
    logger.info('Each record must have a unique identifier\n')

    customer_id = CharField(primary_key=True, max_length=10)
    name = CharField(max_length=30)
    lastname = CharField(max_length=30)
    home_addr = CharField(max_length=40)
    phone_number = CharField(max_length=30)
    email = CharField(max_length=40)
    status = BooleanField()
    cred_limit = DecimalField(max_digits=6, decimal_places=2)
