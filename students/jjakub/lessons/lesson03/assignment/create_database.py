# Create Database
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
"""
Module to create a database and define the Customer model
"""

from peewee import *

TABLE_NAME = 'customers'
DATABASE = SqliteDatabase(TABLE_NAME + '.db')


def main():
    """ This fucntions initiates the database connect and creates a table """
    DATABASE.connect()
    DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
    if Customer.table_exists() is False:
        Customer.create_table()
        print(f"{TABLE_NAME} table created successfully")
    else:
        print(f"{TABLE_NAME} table already exists")
    DATABASE.close()


class BaseModel(Model):
    """ This class defines BaseModel """
    class Meta:
        """ This class defines the database """
        database = DATABASE


class Customer(BaseModel):
    """
    This class defines Customer, which maintains details of someone
    who has made a purchase
    """
    customer_id = CharField(primary_key=True, max_length=7)
    name = CharField(max_length=20)
    lastname = CharField(max_length=20, null=True)
    address = CharField(max_length=40, null=True)
    phone_number = CharField(max_length=40, null=True)
    email = CharField(max_length=40, null=True)
    status = CharField(max_length=8, null=True)
    credit_limit = IntegerField(null=True)
