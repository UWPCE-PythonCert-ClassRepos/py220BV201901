""" Functions to operate on HP Norton database """

from peewee import *
import logging
from hpnortondbmodel import BaseModel, Customer


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

DATABASE = SqliteDatabase('hpnorton.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

def create_sqlite_database():
    """ Used to create sqlite database on initilization """

    DATABASE.create_tables([
        Customer
    ])

def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    """
    Adds a new customer to the customer database
    """

    try:
        with DATABASE.transaction():
            new_customer = Customer.create(
                customer_id = customer_id,
                customer_name = name,
                customer_lastname = lastname,
                customer_home_address = home_address,
                customer_phone_number = phone_number,
                customer_email = email_address,
                customer_status = status,
                customer_credit_limit = credit_limit)
            new_customer.save()

        LOGGER.info(f'Customer {customer_id} successfully added to database.')
    except Exception as db_exception:
        LOGGER.error(f'Customer {customer_id} failed to be added to database.')
        LOGGER.error(f'Exception: {type(db_exception).__name__}')


def search_customer(customer_id):
    """
    Returns dictionary object with name, lastname, email and phone.
    Returns empty object if customer not found.
    """
    try:
        found_customer = Customer.get(customer_id=customer_id)
        LOGGER.info(f'Customer {customer_id} found successfully.')

        return {'name': found_customer.customer_name, 'lastname': found_customer.customer_lastname, 'email':                found_customer.customer_email, 'phone': found_customer.customer_phone_number}

    except DoesNotExist:
        LOGGER.warn(f'Customer {customer_id} not found in database')
        return {}


def delete_customer(customer_id):
    """
    Deletes a customer from the database.
    """

    # success
    LOGGER.info(f'Customer {customer_id} successfully deleted.')
    # failure
    LOGGER.info(f'Customer {customer_id} failed deletion.')
    pass


def update_customer_credit(customer_id, credit_limit):
    """
    Updates customer credit limit.
    """

    # success
    LOGGER.info(f'Customer {customer_id} successfully updated.')
    # failure
    LOGGER.info(f'Customer {customer_id} failed update.')
    pass


def list_active_customers():
    """
    Returns the number of active customers.
    """

    LOGGER.info(f'Active customer check in list_active_customers')
    pass
