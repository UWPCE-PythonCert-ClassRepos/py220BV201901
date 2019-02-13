# Basic Operation
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
"""
Module to define the the basic operations
"""

import csv
import logging
import datetime
from peewee import *
from create_database import *

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.WARNING)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER.setLevel(logging.DEBUG)

LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.setLevel("DEBUG")


def load_csv(file_name):
    """ Load CSV to Customer database """
    try:
        with open(file_name, 'r') as cust_data:
            next(cust_data)
            cust_list = list(csv.reader(cust_data))

        with DATABASE.atomic():
            for batch in chunked(cust_list, 100):
                Customer.insert_many(batch, [Customer.customer_id,
                                             Customer.name,
                                             Customer.last_name,
                                             Customer.home_address,
                                             Customer.phone_number,
                                             Customer.email_address,
                                             Customer.status,
                                             Customer.credit_limit]).execute()
                LOGGER.debug("Batch loaded successfully")
    except FileNotFoundError:
        LOGGER.error("File % does not exist", file_name)
    except IntegrityError:
        cust_fail = [item[0] for item in batch]
        LOGGER.error("Load Failed: At least one of the Customer ID's already exists %"
                     , cust_fail)


def add_customer(customer_id, name, last_name, home_address, phone_number,
                 email_address, status, credit_limit):
    """ Add new customer to Customer table """
    with DATABASE.transaction():
        try:
            new_cust = Customer.create(customer_id=customer_id,
                                       name=name,
                                       last_name=last_name,
                                       home_address=home_address,
                                       phone_number=phone_number,
                                       email_address=email_address,
                                       status=status,
                                       credit_limit=credit_limit)
            new_cust.save()
            cust_list = [customer_id, name, last_name, home_address, phone_number,
                         email_address, status, credit_limit]
            LOGGER.debug("Loaded successful: %", cust_list)
        except IntegrityError:
            LOGGER.error("Load failed: Customer ID % already exists", customer_id)
            raise ValueError


def search_customer(customer_id):
    """ Search for customer in the Customer table """
    try:
        cust_dict = Customer.select().dicts().where(Customer.customer_id == customer_id)[0]
        return_dict = dict((key, value) for key, value in cust_dict.items()
                           if key in ('customer_id', 'name', 'last_name',
                                      'phone_number', 'email_address'))
        LOGGER.debug("Search successful: Customer ID % found", return_dict)
    except IndexError:
        return_dict = {}
        LOGGER.error("Seach failed: Customer ID % does not exist", customer_id)
    return return_dict


def delete_customer(customer_id):
    """ Delete customer in the Customer table """
    remove_cust = Customer.delete().where(Customer.customer_id == customer_id)
    LOGGER.debug("Deletion successful: Customer ID % removed", customer_id)
    return remove_cust.execute()


def update_customer_credit(customer_id, credit_limit):
    """ Update a customers credit limit in Customer table """
    update_cust = Customer.update(credit_limit=credit_limit).where(Customer.customer_id ==
                                                                   customer_id)
    LOGGER.debug("update successful: credit limit for Customer ID % updated", customer_id)
    return update_cust.execute()


def list_active_customers():
    """ Count of all customers in Customer table with a status of Active """
    cust_cnt = Customer.select().where(Customer.status == 'Active').count()
    return cust_cnt
