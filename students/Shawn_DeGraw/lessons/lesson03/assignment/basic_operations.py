""" Functions to operate on HP Norton database """

from peewee import *
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    """
    Adds a new customer to the customer database
    """

    logger.info(f'Customer {customer_id} successfully added to database.')
    pass


def search_customer(customer_id):
    """
    Returns dictionary object with name, lastname, email and phone.
    Returns empty object if customer not found.
    """
    # success
    logger.info(f'Customer {customer_id} found successfully.')
    # failure
    logger.info(f'Customer {customer_id} not found in database')
    pass


def delete_customer(customer_id):
    """
    Deletes a customer from the database.
    """

    # success
    logger.info(f'Customer {customer_id} successfully deleted.')
    # failure
    logger.info(f'Customer {customer_id} failed deletion.')
    pass


def update_customer_credit(customer_id, credit_limit):
    """
    Updates customer credit limit.
    """

    # success
    logger.info(f'Customer {customer_id} successfully updated.')
    # failure
    logger.info(f'Customer {customer_id} failed update.')
    pass


def list_active_customers():
    """
    Returns the number of active customers.
    """

    logger.info(f'Active customer check in list_active_customers')
    pass
