""" Unit tests for assignment01 """
from unittest import TestCase

from basic_operations import add_customer
from basic_operations import search_customer
from basic_operations import delete_customer
from basic_operations import update_customer_credit
from basic_operations import list_active_customers
from basic_operations import util_drop_tables

from loguru import logger
from sys import stdout

logger.add(stdout, level='DEBUG')
logger.enable(__name__)

test_customer_id = 1234
test_new_credit_limit = 3000.00
test_data = {
    'name' : 'Greg',
    'lastname' : 'Smith',
    'home_address' : '123 Main St., Bothell, WA 98104',
    'phone_number' : '(425) 555-1212',
    'email_address' : 'greg.smith@email.com',
    'status' : True,
    'credit_limit' : 1500.00
}


class BasicOpsTest(TestCase):
    """Basic Operations test"""
    def test_add_customer(self):
        """ Test adding a customer  """
        global test_data, test_customer_id

        try:
            add_customer(test_customer_id, test_data)
        except ValueError:
            self.fail(f'Customer id {test_customer_id} not found')

        try:
            db_dict = search_customer(test_customer_id)
        except ValueError:
            self.fail(f'Customer id {test_customer_id} not found')

        self.assertNotEquals(db_dict, {})
        self.assertEqual(test_data['name'], db_dict['name'])
        self.assertEqual(test_data['lastname'], db_dict['lastname'])
        self.assertEqual(test_data['email_address'], db_dict['email_address'])
        self.assertEqual(test_data['phone_number'], db_dict['phone_number'])
    

    def test_search_customer(self):
        """ Test querying a customer """
        try:
            db_dict = search_customer(test_customer_id)
        except ValueError:
            self.fail(f'Customer id {test_customer_id} not found')

        self.assertNotEquals(db_dict, {})
        self.assertEqual(test_data['name'], db_dict['name'])
        self.assertEqual(test_data['lastname'], db_dict['lastname'])
        self.assertEqual(test_data['email_address'], db_dict['email_address'])
        self.assertEqual(test_data['phone_number'], db_dict['phone_number'])


    def test_update_customer_credit(self):
        """ Test updating a customer credit limit"""
        try:
            new_credit_limit = update_customer_credit(test_customer_id, test_new_credit_limit)
        except ValueError:
            self.fail(f'Customer id {test_customer_id} not found')

        self.assertEqual(new_credit_limit, test_new_credit_limit)

    def test_list_active_customers(self):
        """ Test list active customers """
        try:
            num_customers = list_active_customers()
        except ValueError:
            assert False
        self.assertEqual(num_customers, 1)


    def test_delete_customer(self):
        """ Test deleting a customer """
        try:
            delete_customer(test_customer_id)
        except ValueError:
            self.fail(f'Customer id {test_customer_id} not found')

        try:
            num_customers = list_active_customers()
        except ValueError:
            self.fail(f'Customer id {test_customer_id} not found')

        self.assertEqual(num_customers, 0)
