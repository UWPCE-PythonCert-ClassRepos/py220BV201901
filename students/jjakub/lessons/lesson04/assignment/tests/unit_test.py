# Unit Test
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
"""
Module to define the unit tests for the Basic Operations module
"""

import logging
import datetime
from unittest import TestCase
from basic_operations import *
from timeit import default_timer as timer


LOGGER.setLevel(logging.DEBUG)

TEST_CUST = ('test_001', 'test_name', 'test_last_name', 'test_address',
             'test_phone_number', 'test_email', 'active', 100)

TEST_INVALID = ('test_001', 'test_name', 'test_last_name', 'test_address',
                'test_phone_number', 'test_email', 'active', 'five')

SEARCH_TEST = {'name': 'test_name',
               'lastname': 'test_last_name',
               'email': 'test_email',
               'phone_number': 'test_phone_number'}


class CustomerTest(TestCase):
    """ Customer test class """


    def test_table_exists(self):
        """ Table exists """
        assert Customer.table_exists()


    def test_load_csv(self):
        self.assertEqual(list_all_customers(), 0)

        load_csv("customer.csv")
        self.assertEqual(list_all_customers(), 10000)

        delete_all()

        self.assertEqual(list_all_customers(), 0)


    def test_add_customer(self):
        """ Add new customer test """
        add_customer(TEST_CUST[0],
                     TEST_CUST[1],
                     TEST_CUST[2],
                     TEST_CUST[3],
                     TEST_CUST[4],
                     TEST_CUST[5],
                     TEST_CUST[6],
                     TEST_CUST[7])

        cust_dict = search_customer(TEST_CUST[0])
        self.assertEqual(SEARCH_TEST, cust_dict)

        delete_customer(TEST_CUST[0])
        cust_dict = search_customer(TEST_CUST[0])
        self.assertEqual({}, cust_dict)


    def test_add_integrity(self):
        """ Test adding invalid data types """
        add_customer(TEST_INVALID[0],
                     TEST_INVALID[1],
                     TEST_INVALID[2],
                     TEST_INVALID[3],
                     TEST_INVALID[4],
                     TEST_INVALID[5],
                     TEST_INVALID[6],
                     TEST_INVALID[7])

        cust_num = search_customer("test_001")
        self.assertEqual({}, cust_num)


    def test_add_existing_customer(self):
        """ Test add existing customer """
        add_customer(TEST_CUST[0],
                     TEST_CUST[1],
                     TEST_CUST[2],
                     TEST_CUST[3],
                     TEST_CUST[4],
                     TEST_CUST[5],
                     TEST_CUST[6],
                     TEST_CUST[7])

        cust_dict = search_customer(TEST_CUST[0])
        self.assertEqual(SEARCH_TEST, cust_dict)

        add_customer(TEST_CUST[0],
                     TEST_CUST[1],
                     TEST_CUST[2],
                     TEST_CUST[3],
                     TEST_CUST[4],
                     TEST_CUST[5],
                     TEST_CUST[6],
                     TEST_CUST[7])

        self.assertEqual(list_all_customers(), 1)

        delete_customer(TEST_CUST[0])
        cust_dict = search_customer(TEST_CUST[0])
        self.assertEqual({}, cust_dict)


    def test_search_nonexist_customer(self):
        """ Test search customer """
        cust_num = search_customer("NoCustomer")
        self.assertEqual({}, cust_num)


    def test_update_customer_credit(self):
        """ Test update customer credit """
        add_customer(TEST_CUST[0],
                     TEST_CUST[1],
                     TEST_CUST[2],
                     TEST_CUST[3],
                     TEST_CUST[4],
                     TEST_CUST[5],
                     TEST_CUST[6],
                     TEST_CUST[7])

        update_customer_credit(TEST_CUST[0], 999)
        cust_dict = Customer.get(Customer.customer_id == TEST_CUST[0])
        self.assertEqual(cust_dict.credit_limit, 999)

        delete_customer(TEST_CUST[0])
        cust_dict = search_customer(TEST_CUST[0])
        self.assertEqual({}, cust_dict)
