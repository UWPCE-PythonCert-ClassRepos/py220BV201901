# Create database
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
"""
Module to create a database and define the Customer model
"""

from peewee import *

DATABASE = SqliteDatabase('customers.db')


class BaseModel(Model):
    """
    This class defines BaseModel
    """
    class Meta:
        """ This class defines the database """
        database = DATABASE


class Customer(BaseModel):
    """
    This class defines Customer, which maintains details of someone
    who has made a purchase
    """
    customer_id = CharField(primary_key=True, max_length=7, null=False)
    name = CharField(max_length=20)
    last_name = CharField(max_length=20, null=True)
    home_address = CharField(max_length=40, null=True)
    phone_number = CharField(max_length=40, null=True)
    email_address = CharField(max_length=40, null=True)
    status = CharField(max_length=8, null=True)
    credit_limit = IntegerField(null=True)

if __name__ == "__main__":
    DATABASE.connect()
    DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
    if Customer.table_exists() == False:
        Customer.create_table()
    else:
        print("Table already exists, tests not performed")
        sys.exit()
    DATABASE.close()
