# Unit Test
"""
Module to define the unit tests for the Basic Operations module
"""

import sys
from unittest import TestCase
from basic_operations import *
import csv

TEST_01 = ('test_001', 'test_name', 'test_last_name', 'test_address',
           'test_phone_number', 'test_email', 'test_status', 000)

TEST_02 = ('test_002', 'test_name', 'test_last_name', 'test_address',
           'test_phone_number', 'test_email', 'test_status', 000)

TEST_03 = ('test_003', 'test_name', 'test_last_name', 'test_address',
           'test_phone_number', 'test_email', 'test_status', 000)

ADD_DICT_TEST = {'customer_id': 'test_004',
                 'name': 'test_name',
                 'last_name': 'test_last_name',
                 'home_address': 'test_address',
                 'phone_number': 'test_phone_number',
                 'email_address': 'test_email',
                 'status': 'test_status',
                 'credit_limit': 000}

SEARCH_DICT_TEST = {'customer_id': 'test_001',
                    'name': 'test_name',
                    'last_name': 'test_last_name',
                    'phone_number': 'test_phone_number',
                    'email_address': 'test_email'}

UPDATE_DICT_TEST = {'customer_id': 'test_003',
                    'name': 'test_name',
                    'last_name': 'test_last_name',
                    'home_address': 'test_address',
                    'phone_number': 'test_phone_number',
                    'email_address': 'test_email',
                    'status': 'test_status',
                    'credit_limit': 456}

CUST_LIST_TEST = {TEST_01, TEST_02, TEST_03}


class CustomerTest(TestCase):
    """ Customer test class """


    def setUp(self):
        """ Add test records to table """
        with DATABASE.atomic():
            Customer.insert_many(CUST_LIST_TEST, [Customer.customer_id,
                                                  Customer.name,
                                                  Customer.last_name,
                                                  Customer.home_address,
                                                  Customer.phone_number,
                                                  Customer.email_address,
                                                  Customer.status,
                                                  Customer.credit_limit]).execute()


    def tearDown(self):
        """ Delete all test records from table """
        Customer.delete().execute()


    def test_table_exists(self):
        """ Table exists """
        assert Customer.table_exists()


    def test_add_customer(self):
        """ Add new customer test """
        add_customer('test_004', 'test_name', 'test_last_name', 'test_address',
                     'test_phone_number', 'test_email', 'test_status', 000)
        cust_dict = Customer.select().dicts().where(Customer.customer_id == 'test_004')[0]
        self.assertEqual(ADD_DICT_TEST, cust_dict)


    def test_add_existing_customer(self):
        """ Test add existing customer raises """
        with self.assertRaises(ValueError):
            add_customer('test_001', 'test_name', 'test_last_name',
                         'test_address', 'test_phone_number', 'test_email',
                         'test_status', 000)


    def test_search_customer(self):
        """ Test search for existing customer """
        cust_dict = search_customer('test_001')
        self.assertEqual(SEARCH_DICT_TEST, cust_dict)


    def test_search_exist_customer(self):
        """ Test search for non-existing customer """
        cust_dict = search_customer('no_customer_id')
        self.assertEqual({}, cust_dict)


    def test_delete_customer(self):
        """ Test delete customer """
        remove_cust = delete_customer('test_002')
        self.assertEqual(remove_cust, 1)
        with self.assertRaises(IndexError):
            Customer.select().dicts().where(Customer.customer_id == 'test_002')[0]


    def test_update_customer_credit(self):
        """ Test update customer credit """
        update_customer_credit('test_003', 456)
        cust_dict = Customer.select().dicts().where(Customer.customer_id == 'test_003')[0]
        self.assertEqual(UPDATE_DICT_TEST, cust_dict)


    def test_list_active_customers(self):
        """ Test count customers with status active """
        cust_cnt_test = Customer.select().where(Customer.status == 'Active').count()
        cust_cnt = list_active_customers()
        self.assertEqual(cust_cnt_test, cust_cnt)
