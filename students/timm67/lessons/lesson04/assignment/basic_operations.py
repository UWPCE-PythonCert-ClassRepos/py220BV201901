"""
    Basic database operations corresponding to the customer model
    defined in basic
"""

import sys
from loguru import logger
from customer_model import Customer
from customer_model import PhoneInfo
from customer_model import database


logger.add(sys.stdout, level='DEBUG')
logger.add("logfile_{time}.txt", level='DEBUG')
logger.enable(__name__)


def add_customer(**kwargs):
    """
    This function will add a new customer to the sqlite3 database. keyword
    args to keep pylint happy are the following:

    name, lastname, home_address, phone_number,
    email_address, status, credit_limit

    Ensure you application will create an empty database if one doesn’t exist
    when the app is first run. Call it customers.db
    """
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite
        with database.transaction():
            new_cust = Customer.create(
                customer_id=kwargs['customer_id'],
                name=kwargs['name'],
                lastname=kwargs['lastname'],
                home_address=kwargs['home_address'],
                phone_info=kwargs['phone_number'],
                email_address=kwargs['email_address'],
                status=True if kwargs['status'] == 'Active' else False,
                credit_limit=kwargs['credit_limit'])
            new_cust.save()
    except KeyError:
        logger.error('kwargs not complete')
        raise ValueError
    except Exception as thrown_exception:
        logger.info(f'Error creating customer')
        logger.info(thrown_exception)
        logger.info('See how the database protects our data')
    finally:
        logger.info('Database add successful; closing database')
        database.close()
        # close database


def search_customer(customer_id):
    """
    This function will return a dictionary object with name, lastname,
    email address and phone number of a customer or an empty dictionary
    object if no customer was found.
    """
    ret_dict = {}
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite
        with database.transaction():
            cust = Customer.get(Customer.customer_id == customer_id)
            if cust is not None:
                ret_dict['name'] = cust.name
                ret_dict['lastname'] = cust.lastname
                ret_dict['email_address'] = cust.email_address
                ret_dict['phone_number'] = cust.phone_info
                logger.info('Database query successful')
            else:
                logger.error(f'Customer {customer_id} not found')
                raise ValueError
    except Exception as thrown_exception:
        logger.info(f'Error querying {customer_id}')
        logger.info(thrown_exception)
        logger.info('See how the database protects our data')
    finally:
        database.close()

    return ret_dict


def delete_customer(customer_id):
    """
    This function will delete the record of a customer matching
    customer_id
    """
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite
        with database.transaction():
            cust = Customer.get(Customer.customer_id == customer_id)
            if cust is not None:
                cust.delete_instance()
                logger.info('Database delete successful')
            else:
                logger.error(f'Customer {customer_id} not found')
                raise ValueError
    except Exception as thrown_exception:
        logger.info(f'Error getting {customer_id}')
        logger.info(thrown_exception)
        logger.info('See how the database protects our data')
    finally:
        database.close()


def update_customer_credit(customer_id, credit_limit):
    """
    This function will search an existing customer by customer_id
    and update their credit limit or raise a ValueError exception
    if the customer does not exist.

    The credit limit stored in the database is returned as a float.
    The value is 0.0 if the customer_id is not valid. The value is
    the current value in the database if it _cannot_ be updated,
    else it is the updated value stored in the databsae
    """
    ret_credit = float(0.0)

    if credit_limit < 0.0:
        logger.info(f'Error setting credit limit for {customer_id}')
        logger.info(f'Credit limit is below 0: {credit_limit}')
        raise ValueError

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite
        with database.transaction():
            cust = Customer.get(Customer.customer_id == customer_id)
            if cust is not None:
                ret_credit = cust.credit_limit
                logger.info(f'Updating credit limit from {cust.credit_limit} \
                              to {credit_limit}')
                cust.credit_limit = credit_limit
                ret_credit = cust.credit_limit
                cust.save()
                logger.info('Database update successful')
            else:
                logger.error(f'Customer {customer_id} not found')
                raise ValueError
    except Exception as thrown_exception:
        logger.info(f'Error querying {customer_id}')
        logger.info(thrown_exception)
        logger.info('See how the database protects our data')
    finally:
        database.close()

    return ret_credit


def list_active_customers():
    """
    This function will return an integer with the number of
    customers whose status is currently active.
    """
    active_cust = 0

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite
        for cust in Customer.select().where(Customer.status != 0):
            logger.info(f'Customer {cust.customer_id} is active')
            active_cust += 1
            logger.debug(f"active_cust: {active_cust}")
        logger.info('Database query successful')
    except Exception as thrown_exception:
        logger.info(f'Error querying database')
        logger.info(thrown_exception)
        logger.info('See how the database protects our data')
    finally:
        database.close()

    return active_cust


def util_drop_tables():
    """
    Utility function that drops tables after testing
    """
    tables = [Customer, PhoneInfo]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite
        database.drop_tables(tables)
        logger.info('Database table drop successful')
    except Exception as thrown_exception:
        logger.info('Error dropping Customer table')
        logger.info(thrown_exception)
        logger.info('See how the database protects our data')
    finally:
        database.close()
