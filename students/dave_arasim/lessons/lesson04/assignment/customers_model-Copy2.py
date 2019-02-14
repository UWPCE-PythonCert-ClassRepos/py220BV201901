'''
Database schema definition for customers database 'customers.db'
'''

import datetime
import logging
from peewee import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)

log_file = 'basic_operations'+datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

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
