# Basic Operation
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=no-value-for-parameter
"""
Module to define the the basic operations
"""

import csv
import logging
import datetime
from timeit import default_timer as timer
from peewee import *
from create_database import *

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)


def load_csv(file_name):
    """ Load CSV to Customer database """
    start_time = timer()
    try:
        with open(file_name, 'r') as cust_data:
            next(cust_data)
            cust_list = list(csv.reader(cust_data))

        with DATABASE.atomic():
            for batch in chunked(cust_list, 100):
                Customer.insert_many(batch, [Customer.customer_id,
                                             Customer.name,
                                             Customer.lastname,
                                             Customer.address,
                                             Customer.phone_number,
                                             Customer.email,
                                             Customer.status,
                                             Customer.credit_limit]).execute()
        end_time = timer()
        run_time = round(end_time - start_time, 4)
        LOGGER.debug("Time elapsed %s", run_time)
        LOGGER.debug("Batch loaded successfully")
    except FileNotFoundError:
        LOGGER.error("File %s does not exist", file_name)
    except IntegrityError:
        LOGGER.error("Load Failed: At least one of the Customer ID's already exists")


def add_customer(customer_id, name, lastname, address, phone_number,
                 email, status, credit_limit):
    """ Add new customer to customer table """
    with DATABASE.transaction():
        try:
            new_cust = Customer.create(
                customer_id=customer_id,
                name=name,
                lastname=lastname,
                address=address,
                phone_number=phone_number,
                email=email,
                status=status,
                credit_limit=credit_limit)
            new_cust.save()
            LOGGER.debug("Customer ID %s successfully added", customer_id)
        except IntegrityError:
            LOGGER.warning("Customer ID %s already exists", customer_id)
        except ValueError:
            LOGGER.warning("Customer ID %s has invalid data type", customer_id)


def search_customer(customer_id):
    """ Search for customer in the Customer table """
    try:
        search_id = Customer.get(Customer.customer_id == customer_id)
        LOGGER.debug("Customer ID %s found", customer_id)

        cust_dict = {"name": search_id.name, "lastname": search_id.lastname,
                     "email": search_id.email, "phone_number": search_id.phone_number}
        return cust_dict
    except DoesNotExist:
        LOGGER.warning("Customer ID %s not found", customer_id)
        return {}


def delete_customer(customer_id):
    """ Delete customer in the Customer table """
    start_time = timer()
    try:
        remove_cust = Customer.get(Customer.customer_id == customer_id)
        remove_cust.delete_instance()
        LOGGER.debug("Customer ID %s successfully deleted", customer_id)
        end_time = timer()
        run_time = round(end_time - start_time, 4)
        LOGGER.debug("Time elapsed %s", run_time)
        return True
    except DoesNotExist:
        LOGGER.warning("Customer ID %s not found", customer_id)
    except OperationalError:
        LOGGER.warning("Customer ID %s not found", customer_id)


def update_customer_credit(customer_id, credit_limit):
    """ Update a customers credit limit in Customer table """
    try:
        Customer.get(Customer.customer_id == customer_id)
        update_cust = Customer.update(credit_limit=credit_limit).where(Customer.customer_id ==
                                                                       customer_id)
        LOGGER.debug("Credit limit for Customer ID %s updated to", credit_limit)
        update_cust.execute()
    except DoesNotExist:
        LOGGER.warning("Customer ID %s not found", customer_id)
        raise ValueError('NoCustomer')


def list_active_customers():
    """ Count of all customers in Customer table with a status of Active """
    cust_cnt = Customer.select().where(Customer.status == 'active'
                                       or Customer.status == 'Active').count()
    LOGGER.debug("There are %s active customers in the table", cust_cnt)
    return cust_cnt


def list_all_customers():
    """ Count of all customers in Customer table """
    cust_cnt = Customer.select().count()
    LOGGER.debug("There are %s total customers in the table", cust_cnt)
    return cust_cnt


def delete_all():
    """ Remove all customers in Customer table """
    remove_cnt = Customer.select().count()
    remove_data = Customer.delete()
    LOGGER.debug("All data removed: %s rows", remove_cnt)
    remove_data.execute()

if __name__ == "__main__":
    main()
