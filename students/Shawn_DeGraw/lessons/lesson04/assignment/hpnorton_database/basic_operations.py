""" Functions to operate on HP Norton database """


import logging
from peewee import *
from lesson04.assignment.hpnorton_database.hpnortondbmodel import *


LOG_FORMAT = "%(asctime)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE_DB = 'db.log'
LOG_FILE_SYSTEM = 'system.log'

FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER_DB = logging.FileHandler(LOG_FILE_DB, mode='w')
FILE_HANDLER_DB.setFormatter(FORMATTER)

FILE_HANDLER_SYSTEM = logging.FileHandler(LOG_FILE_SYSTEM, mode='w')
FILE_HANDLER_SYSTEM.setFormatter(FORMATTER)

# Database access logging
DBLOG = logging.getLogger('DBLOG')
DBLOG.addHandler(FILE_HANDLER_DB)
DBLOG.setLevel("INFO")

# General logging
SYSTEMLOG = logging.getLogger('SYSTEMLOG')
SYSTEMLOG.addHandler(FILE_HANDLER_SYSTEM)
SYSTEMLOG.setLevel("INFO")


def file_to_database(custfile):
    """
    Reads a file and adds records to database.

    Param: filename
    """

    try:

        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

        with open(custfile, 'r') as filename:
            for line in filename:
                try:
                    linelist = line.rstrip().split(',')

                    with DATABASE.transaction():
                        new_customer = Customer.create(
                            customer_id=linelist[0],
                            name=linelist[1],
                            lastname=linelist[2],
                            home_address=linelist[3],
                            phone_number=linelist[4],
                            email=linelist[5],
                            status=linelist[6].lower(),
                            credit_limit=int(linelist[7]))
                        new_customer.save()

                    DBLOG.info(f'Added to database: {linelist}')

                except IntegrityError as db_exception:
                    DBLOG.error(f'Customer data failed entry {linelist}')
                    SYSTEMLOG.error(f'Exception: {type(db_exception).__name__}')

                except ValueError as data_error:
                    SYSTEMLOG.error(f'Data error for: {linelist}')
                    SYSTEMLOG.error(f'Exception: {type(data_error).__name__}')
                    continue

                except AttributeError as data_error:
                    SYSTEMLOG.error(f'Data error for: {linelist}')
                    SYSTEMLOG.error(f'Exception: {type(data_error).__name__}')
                    continue

    except IOError as db_fileerror:
        SYSTEMLOG.error(f'File exception: {type(db_fileerror).__name__}')

    except OperationalError as db_fileerror:
        SYSTEMLOG.error(f'Database exception: {type(db_fileerror).__name__}')

    finally:
        DATABASE.close()



def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    """
    Adds a new customer to the customer database:

    Arguments:
    customer_id - unique id representing customer
    name - customer first name
    lastname - customer last name
    home_address - customer home address
    phone_number - customer telephone number
    email_address - customer email
    status - active or inactive
    credit_limit - integer value
    """

    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

        with DATABASE.transaction():
            new_customer = Customer.create(
                customer_id=customer_id,
                name=name,
                lastname=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email=email_address,
                status=status.lower(),
                credit_limit=credit_limit)
            new_customer.save()

        DBLOG.info(f'Customer {customer_id} successfully added to database.')

    except IntegrityError as db_exception:
        DBLOG.error(f'Customer {customer_id} failed to be added to database.')
        SYSTEMLOG.error(f'Exception: {type(db_exception).__name__}')

    except AttributeError as data_error:
        SYSTEMLOG.error(f'Data error: {type(data_error).__name__}')

    finally:
        DATABASE.close()


def search_customer(customer_id):
    """
    Returns dictionary object with name, lastname, email and phone.
    Returns empty object if customer not found.
    """
    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

        found_customer = Customer.get(Customer.customer_id == customer_id)
        DBLOG.info(f'Customer {customer_id} found successfully.')

        DATABASE.close()
        return {'name': found_customer.name, 'lastname': found_customer.lastname, 'email': found_customer.email, 'phone_number': found_customer.phone_number}

    except DoesNotExist:
        DBLOG.warning(f'Customer {customer_id} not found in database')
        DATABASE.close()
        return {}

    except InternalError:
        SYSTEMLOG.error('Database error.')
        DATABASE.close()
        return {}

def search_lastname(srchlastname):
    """
    Returns dictionary object with customer id, name, lastname, email and phone.
    Returns empty object if customer not found.
    Query could return more than one object.
    """

    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

        query = Customer.select(Customer.customer_id,
                                Customer.name,
                                Customer.lastname,
                                Customer.email,
                                Customer.phone_number
                                ).where(Customer.lastname == srchlastname).dicts()

        DBLOG.info(f'Found {sum(1 for line in query)} customers for name {srchlastname}.')

        DATABASE.close()
        return query

    except Exception as dberror:
        DBLOG.warning(f'Customer search by last name failed.')
        SYSTEMLOG.warning(f'Exception: {type(dberror).__name__}')
        DATABASE.close()
        return {}


def delete_customer(customer_id):
    """
    Deletes a customer from the database.
    """

    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

        with DATABASE.transaction():
            found_customer = Customer.get(Customer.customer_id == customer_id)
            found_customer.delete_instance()

        DBLOG.info(f'Customer {customer_id} successfully deleted.')

    except DoesNotExist:
        DBLOG.warning(f'Customer {customer_id} failed deletion.')

    except InternalError:
        SYSTEMLOG.error('Database error.')
        DATABASE.close()

    finally:
        DATABASE.close()


def update_customer_credit(customer_id, credit_limit):
    """
    Updates customer credit limit.
    """

    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

        with DATABASE.transaction():
            customer_found = Customer.get(Customer.customer_id == customer_id)
            customer_found.credit_limit = credit_limit
            customer_found.save()

        DBLOG.info(f'Customer {customer_id} successfully updated.')

    except DoesNotExist:
        DBLOG.info(f'Customer {customer_id} failed update.')
        raise ValueError('NoCustomer')

    except InternalError:
        SYSTEMLOG.error('Database error.')
        DATABASE.close()

    finally:
        DATABASE.close()


def list_active_customers():
    """
    Returns the number of active customers.
    """

    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

        actcount = Customer.select().where(Customer.status == 'active').count()
        # status should be lower case, controlled on db save
        DBLOG.info(f'Active customer check in list_active_customers: {actcount}')

    except Exception as dberror:
        SYSTEMLOG.warning(f'Database error occured: {type(dberror).__name__}')

    finally:
        DATABASE.close()

    return actcount


def total_db_record_count():
    """
    Returns the count of records in the database.
    """

    totcount = 0

    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

        totcount = Customer.select().count()

    except (InternalError, OperationalError):
        SYSTEMLOG.error('Database error.')

    finally:
        DATABASE.close()

    return totcount


def search_kwarg(custfield, custvalue):
    """
    Database search using key word argument matching db field
    """

    searchfield = f'Customer.{custfield}'
    
    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

        query = Customer.select(Customer.customer_id,
                                Customer.name,
                                Customer.lastname,
                                Customer.email,
                                Customer.phone_number
                                ).where(getattr(Customer, custfield) == custvalue).dicts()

        DBLOG.info(f'Found {sum(1 for line in query)} customers for {searchfield} = {custvalue}.')

        DATABASE.close()
        return query

    except Exception as dberror:
        DBLOG.warning(f'Customer search failed.')
        SYSTEMLOG.warning(f'Exception: {type(dberror).__name__}')
        DATABASE.close()
        return {}
