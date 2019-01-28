""" Functions to operate on HP Norton database """


import logging
from peewee import *
from lesson03.assignment.hpnorton_database.hpnortondbmodel import *


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    """
    Adds a new customer to the customer database
    """

    try:
        with DATABASE.transaction():
            new_customer = Customer.create(
                customer_id=customer_id,
                name=name,
                lastname=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email=email_address,
                status=status,
                credit_limit=credit_limit)
            new_customer.save()

        LOGGER.info(f'Customer {customer_id} successfully added to database.')

    except IntegrityError as db_exception:
        LOGGER.error(f'Customer {customer_id} failed to be added to database.')
        LOGGER.error(f'Exception: {type(db_exception).__name__}')


def search_customer(customer_id):
    """
    Returns dictionary object with name, lastname, email and phone.
    Returns empty object if customer not found.
    """
    try:
        found_customer = Customer.get(Customer.customer_id == customer_id)
        LOGGER.info(f'Customer {customer_id} found successfully.')

        return {'name': found_customer.name, 'lastname': found_customer.lastname, 'email': found_customer.email, 'phone_number': found_customer.phone_number}

    except DoesNotExist:
        LOGGER.warning(f'Customer {customer_id} not found in database')
        return {}


def search_lastname(srchlastname):
    """
    Returns dictionary object with customer id, name, lastname, email and phone.
    Returns empty object if customer not found.
    Query could return more than one object.
    """

    try:
        query = Customer.select(Customer.customer_id, Customer.name, Customer.lastname, Customer.email, Customer.phone_number).where(Customer.lastname == srchlastname).dicts()

        LOGGER.info(f'Searching for customer last name.')

        return query

    except Exception as dberror:
        LOGGER.warning(f'Customer search by last name failed.')
        LOGGER.warning(f'Exception: {type(dberror).__name__}')
        return {}


def delete_customer(customer_id):
    """
    Deletes a customer from the database.
    """

    try:
        with DATABASE.transaction():
            found_customer = Customer.get(Customer.customer_id == customer_id)
            found_customer.delete_instance()

        LOGGER.info(f'Customer {customer_id} successfully deleted.')

    except DoesNotExist:
        LOGGER.warning(f'Customer {customer_id} failed deletion.')


def update_customer_credit(customer_id, credit_limit):
    """
    Updates customer credit limit.
    """

    try:
        with DATABASE.transaction():
            customer_found = Customer.get(Customer.customer_id == customer_id)
            customer_found.credit_limit = credit_limit
            customer_found.save()

        LOGGER.info(f'Customer {customer_id} successfully updated.')

    except DoesNotExist:
        LOGGER.info(f'Customer {customer_id} failed update.')
        raise ValueError('NoCustomer')


def list_active_customers():
    """
    Returns the number of active customers.
    """

    LOGGER.info(f'Active customer check in list_active_customers')
    return Customer.select().where(Customer.status == 'active').count()
