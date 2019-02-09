""" Unit tests for assignment01 """
import pytest

from basic_operations import add_customer
from basic_operations import search_customer
from basic_operations import delete_customer
from basic_operations import update_customer_credit
from basic_operations import list_active_customers
from basic_operations import util_drop_tables

from loguru import logger
from sys import stdout

logger.add(stdout, level='INFO')
logger.enable(__name__)

test_new_credit_limit = 3000.00
test_customer_id = 1234
test_data = {
    'customer_id' : test_customer_id,
    'name' : 'Greg',
    'lastname' : 'Smith',
    'home_address' : '123 Main St., Bothell, WA 98104',
    'phone_number' : '(425) 555-1212',
    'email_address' : 'greg.smith@email.com',
    'status' : True,
    'credit_limit' : 1500.00
}

def test_01_add_customer():
    """ Test adding a customer  """
    global test_data, test_customer_id

    try:
        add_customer(**test_data)
    except ValueError:
        logger.error(f'Customer id {test_customer_id} not found')

    try:
        db_dict = search_customer(test_customer_id)
    except ValueError:
        logger.error(f'Customer id {test_customer_id} not found')

    assert db_dict != {}
    assert test_data['name'] == db_dict['name']
    assert test_data['lastname'] == db_dict['lastname']
    assert test_data['email_address'] == db_dict['email_address']
    assert test_data['phone_number'] == db_dict['phone_number']


def test_02_search_customer():
    """ Test querying a customer """
    try:
        db_dict = search_customer(test_customer_id)
    except ValueError:
        logger.error(f'Customer id {test_customer_id} not found')

    assert db_dict != {}
    assert test_data['name'] == db_dict['name']
    assert test_data['lastname'] == db_dict['lastname']
    assert test_data['email_address'] == db_dict['email_address']
    assert test_data['phone_number'] == db_dict['phone_number']


def test_03_update_customer_credit():
    """ Test updating a customer credit limit"""
    try:
        new_credit_limit = update_customer_credit(test_customer_id, test_new_credit_limit)
    except ValueError:
        logger.error(f'Customer id {test_customer_id} not found')

    assert new_credit_limit == test_new_credit_limit

def test_04_list_active_customers():
    """ Test list active customers """
    try:
        num_customers = list_active_customers()
    except ValueError:
        assert False
    assert num_customers == 1


def test_05_delete_customer():
    """ Test deleting a customer """
    try:
        delete_customer(test_customer_id)
    except ValueError:
        logger.error(f'Customer id {test_customer_id} not found')

    try:
        num_customers = list_active_customers()
    except ValueError:
        logger.error(f'Customer id {test_customer_id} not found')

    assert num_customers == 0


def test_06_drop_tables():
    logger.info('Dropping tables (cleanup)')
    util_drop_tables()
