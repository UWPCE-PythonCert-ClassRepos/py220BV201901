# Student: Bradnon Nguyen
# Class:   Advance Python 220 - Jan2019
# Lesson03 - basic_operations.py.
"""
Importing customer_db_model.py this file has the following function:
- add_customer.
-search_customer.
-delete_customer.
-update_customer_credit.
-list_active_customers.
"""
import logging
from peewee import *
from lesson03.assignment.customer_db_model import *


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info('Starting program action.')


def initialize_db():
    """
    Create DB to meet requirement # 6.
    Ensure you application will create an empty database if one doesn’t
    exist when the app is first run. Call it customers.db
    """
    try:
        LOGGER.info('Creating Database..')
        DB.connect()
        DB.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only
        Customer.create_table()
    except Exception as errs:
        LOGGER.warning(f'Creating DB issue.  {errs}')

initialize_db()


def db_initial_steps():
    """basic method to reuse sqlite3 connection strings"""
    DB.connect(reuse_if_open=True)
    DB.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only
    LOGGER.info("DB-connection")


def add_customer(customer_id, name, lastname, home_address, phone_number,
                 email_address, status, credit_limit):
    """
    This function will add a new customer to the sqlite3 database.
    Parameters:customer_id, name, lastname, home_address, phone_number,
               email_address, status, credit_limit.
    """
    try:
        db_initial_steps()
        with DB.transaction():
            new_customer = Customer.create(
                customer_id=customer_id,
                name=name,
                lastname=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email=email_address,
                status=status,
                credit_limit=credit_limit
            )
            new_customer.save()
            LOGGER.info(f'SAVE: Customer with id: {customer_id} has been saved.')
    except Exception as errs:
        LOGGER.error(f"SAVE: Failed DATA save on input record id: {customer_id}.")
        LOGGER.error(errs)

    finally:
        DB.close()
        LOGGER.info("DB closed")


def search_customer(customer_id_in):
    """
    This function will return a dictionary object with name, lastname,
    email address and phone number of a customer or an empty
    dictionary object if no customer was found.
    Param: customer_id_in.
    """
    LOGGER.info('Entered search customer.')
    dict_customer = {}  # To hold return values.
    try:
        db_initial_steps()
        searched_customer = Customer.get(Customer.customer_id == customer_id_in)
        LOGGER.info(f'FIND: Customer object with id: {customer_id_in} has been return.')
        dict_customer = {"name": searched_customer.name,
                         "lastname": searched_customer.lastname,
                         "email": searched_customer.email,
                         "phone_number": searched_customer.phone_number
                         }
    except Exception as errs:
        LOGGER.error(f'FIND: Unable to find user: {customer_id_in}.')
        LOGGER.error(errs)

    finally:
        DB.close()
        LOGGER.info("DB closed connection.")
    return dict_customer  # finally we will return value either empty or with data


def delete_customer(customer_id_in):
    """
    This function will delete a customer from the sqlite3 database.
    Param: customer_id
    """
    LOGGER.info('Entered find and delete.')
    try:
        db_initial_steps()
        customer_tb_deleted = Customer.get(Customer.customer_id == customer_id_in)
        customer_tb_deleted.delete_instance()
        LOGGER.info(f'DELETE: Found and removed customer with id: {customer_id_in}.')

    except Exception as errs:
        LOGGER.error(f"Something wrong in deleting {customer_id_in}.")
        LOGGER.error(errs)

    finally:
        DB.close()
        LOGGER.info("DB closed.")


def update_customer_credit(customer_id_in, credit_limit_update):
    """
    This function will search an existing customer by customer_id and update
    their credit limit or raise a ValueError exception if the customer does not exist.
    Parameters: customer_id_in, credit_limit_update.
    """
    LOGGER.info("Entered customer update credit.")
    try:
        db_initial_steps()
        with DB.transaction():
            customer_tb_updated = Customer.get(Customer.customer_id == customer_id_in)
            customer_tb_updated.credit_limit = credit_limit_update
            customer_tb_updated.save()
        LOGGER.info(f"Success: Update done or customer with id: {customer_id_in}.")

    except Exception as errs:
        LOGGER.error(f"NoCustomer Unable to update customer with id: {customer_id_in}.")
        LOGGER.error(errs)
        raise ValueError("NoCustomer")

    finally:
        DB.close()
        LOGGER.info("Closed DB connection")


def list_active_customers():
    """
    This function will return an integer with the number (count) of customers,
    whose status is currently "active".
    """
    LOGGER.info("Entered active customer count.")
    try:
        db_initial_steps()
        count_active_customer = Customer.select().where(Customer.status == 'active').count()
        LOGGER.info(f'Success: The number of {count_active_customer}')

    except Exception as errs:
        LOGGER.error(f'DBMS issue: {errs}.')

    finally:
        DB.close()
        LOGGER.info("Closed connection in list active customer.")
    return count_active_customer
