# Student: Bradnon Nguyen
# Class:   Advance Python 220 - Jan2019
# Lesson04 - Refactor - basic_operations.py.
"""
Importing customer_db_model.py this file has the following function:
- add_customer.
-search_customer.
-delete_customer.
-update_customer_credit.
-list_active_customers.
"""
import logging
import datetime
import codecs
import csv
from peewee import *
from lesson03.assignment.customer_db_model import *


# logging.basicConfig(level=logging.INFO,)
# LOGGER.info('Starting program action.')


# LOGGING SETTING START
LOG_FORMAT = "%(asctime)s %(filename)s:%(funcName)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d")+'db.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
DICT_LEVEL = {'0': 'disabled', '1': 'ERROR', '2': 'WARNING', '3': 'DEBUG'}

# Log setting for writing to file
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.WARNING)  # Saving to log file via level
FILE_HANDLER.setFormatter(FORMATTER)

# Log setting for display to standout.
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)  # Send log to console: DEBUG level
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)
# LOGGING SETTING END!


def initialize_db(tablename):
    """
    Create DB to meet requirement # 6.
    Ensure you application will create an empty database if one doesn’t
    exist when the app is first run. Call it customers.db
    """
    try:
        LOGGER.info('Creating Database..')
        DB.connect()
        DB.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only
        tablename.create_table()
        LOGGER.info('CREATE: Tablename =  has been created.')
    except Exception as errs:
        LOGGER.warning(f'Creating DB issue.  {errs}')
    DB.close()

# Creating the database with table Customer First!
initialize_db(Customer)


def db_initial_steps():
    """basic method to reuse sqlite3 connection strings"""
    DB.connect(reuse_if_open=True)
    DB.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only
    LOGGER.info("DB-connection")


def process_csv(csv_file_in):
    """
    Read in csv file and return a list of rows.
    Param: csv file name.
    """
    data = []

    with open(csv_file_in, 'r', newline='') as csvfile:
        has_header = csv.Sniffer().has_header(csvfile.read(1024))  # 1024=read 2 lines
        csvfile.seek(0)  # Rewind.
        reader = csv.reader(csvfile)

        if has_header:  # True False
            next(reader)  # Skip header row.
        try:
            for row in reader:
                LOGGER.info(f'CSV: processing the the next row: {row}.')
                yield row
                data.append(row)  # adding the data row into list data

        except csv.Error as errs:
            LOGGER.error(f"Some sort of data process issue: {row}")
            LOGGER.error(errs)

    return data


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
            LOGGER.warning(f'ADD: Customer with id: {customer_id} has been saved.')

    except Exception as errs:
        LOGGER.error(f"ADDFAIL: Failed DATA save on input record id: {customer_id}.")
        LOGGER.error(errs)

    finally:
        DB.close()
        LOGGER.info(f"ADD: DB closed.")


def add_customers(list_in):
    """
    This function is used to add more than 1 customers to the db from a list.
    Param: a list.
    Although the intend of usage here would be add_customers(process_csv(file_name_csv)).
    """
    try:
        for customer in list_in:
            add_customer(customer[0], customer[1], customer[2],
                         customer[3], customer[4], customer[5],
                         customer[6], customer[7]
                         )

    except Exception as eerrs:
        LOGGER.error(f'ADDFAIL: Something went wrong with saving dat from a list: {list_in}.')
        LOGGER.error(eerrs)


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
        LOGGER.error(f'FINDFAIL: Unable to find user: {customer_id_in}.')
        LOGGER.error(errs)

    finally:
        DB.close()
        LOGGER.info(f"FIND:DB closed connection.")

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
        LOGGER.warning(f'DELETE: Found and removed customer with id: {customer_id_in}.')

    except Exception as errs:
        LOGGER.error(f"DELETE:Something wrong in deleting {customer_id_in}.")
        LOGGER.error(errs)

    finally:
        DB.close()
        LOGGER.info(f"DELETE: DB closed.")


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
        LOGGER.warning(f"UPDATE: Update done for customer with id: {customer_id_in}.")

    except Exception as errs:
        LOGGER.error(f"UPDATE: Unable to update customer with id: {customer_id_in}.")
        LOGGER.error(errs)
        raise ValueError("NoCustomer")

    finally:
        DB.close()
        LOGGER.info("UPDATE:Closed DB connection")


def list_active_customers():
    """
    This function will return an integer with the number (count) of customers,
    whose status is currently "active".
    """
    LOGGER.info(f"LISTACTIVE:Entered function.")
    try:
        db_initial_steps()
        count_active_customer = Customer.select().where(Customer.status == 'active').count()
        LOGGER.info(f'LISTACTIVE: The number of {count_active_customer}')

    except Exception as errs:
        LOGGER.error(f'LISTFAIL: DBMS issue: {errs}.')

    finally:
        DB.close()
        LOGGER.info("LISTACTIVE: Closed connection.")
    return count_active_customer


def delete_all_customers(table_name):
    """
    This function is used to delete all records in Customer model.
    Param: Model or Table name.
    """
    LOGGER.info(f"DELETEALL:Entered active customer count.")
    try:
        db_initial_steps()
        table_name.delete()  # delete all
        LOGGER.warning(f'DELETEALL: all customers in {table_name} have been removed.')
    except Exception as errs:
        LOGGER.error(f'DELETEALLFAIL: Something wrong with truncate table {table_name}.')
        LOGGER.error(errs)

    finally:
        DB.close()
        LOGGER.info(f'DELETEALL: DB Closed')
