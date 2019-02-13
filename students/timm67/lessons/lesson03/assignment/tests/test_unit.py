""" Unit tests for assignment03 """
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
test_delete_customer_id = 'C01'
test_data = [
    {
        'customer_id' : 'C01',
        'name' : 'Greg',
        'lastname' : 'Smith',
        'home_address' : '123 Main St., Bothell, WA 98104',
        'phone_number' : '(425) 555-1212',
        'email_address' : 'greg.smith@email.com',
        'status' : 'Active',
        'credit_limit' : 1500.00
    },
    {
        'customer_id' : 'C02',
        'name' : 'Mary',
        'lastname' : 'Smith',
        'home_address' : '123 Main St., Bothell, WA 98104',
        'phone_number' : '(425) 555-1213',
        'email_address' : 'mary.smith@email.com',
        'status' : 'Active',
        'credit_limit' : 1500.00
    }
]


def test_01_add_customers():
    """ Test adding customers  """
    for customer in test_data:
        try:
            add_customer(**customer)
        except ValueError:
            logger.error(f"Customer id { customer['customer_id'] } not found")
            assert False
            return

        try:
            db_dict = search_customer(customer['customer_id'])
        except ValueError:
            logger.error(f"Customer id {customer['customer_id']} not found")
            assert False
            return

        assert db_dict != {}
        assert customer['name'] == db_dict['name']
        assert customer['lastname'] == db_dict['lastname']
        assert customer['email_address'] == db_dict['email_address']
        assert customer['phone_number'] == db_dict['phone_number']


def test_02_search_customer():
    """ Test querying a customer """
    for customer in test_data:
        try:
            db_dict = search_customer(customer['customer_id'])
        except ValueError:
            logger.error(f"Customer id {customer['customer_id']} not found")
            assert False
            return

        assert db_dict != {}
        assert customer['name'] == db_dict['name']
        assert customer['lastname'] == db_dict['lastname']
        assert customer['email_address'] == db_dict['email_address']
        assert customer['phone_number'] == db_dict['phone_number']


def test_03_update_customer_credit():
    """ Test updating a customer credit limit"""
    for customer in test_data:
        try:
            new_credit_limit = update_customer_credit(customer['customer_id'],
                                                      test_new_credit_limit)
        except ValueError:
            logger.error(f"Customer id {customer['customer_id']} not found")
            assert False
            return

        assert new_credit_limit == test_new_credit_limit


def test_04_list_active_customers():
    """ Test list active customers """
    try:
        num_customers = list_active_customers()
    except ValueError:
        assert False
        return

    assert num_customers == len(test_data)


def test_05_delete_customer():
    """ Test deleting a customer """
    try:
        delete_customer(test_delete_customer_id)
    except ValueError:
        logger.error(f'Customer id {test_delete_customer_id} not found')
        assert False
        return

    try:
        num_customers = list_active_customers()
    except Exception as e:
        logger.info(e)
        assert False
        return

    assert num_customers == (len(test_data) - 1)


def test_06_drop_tables():
    """ Test teardown function to drop tables """
    logger.info('Dropping tables (cleanup)')
    util_drop_tables()
