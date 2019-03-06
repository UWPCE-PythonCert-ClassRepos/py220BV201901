#! usr/bin/env python3
""" Testing of basic_operation functions using pytest"""

import pytest
from basic_operations import *
import logging
from peewee import *

data = [('A0001', 'Aaa', 'Zzzz', '123 E Aaaaa NE WA 98102','123-345-6789','aaa.zzzz@abc.com',        'non_active', 1),
        ('A0002', 'Bbbb', 'Yyyy', '4516 W Bbbbbbb SE IL 61614',
        '987-654-1232', 'bbbb.yyyy@xyz.com', 'active', 2000.0),
        ('A0003', 'Cccc', 'Xxxx', '1000 SE Xxxxxx SE WA 98006',
                    '123-000-0001', 'cccc.xxxx@abc.com', 'active', 0)]

def test_new_instance():
    """ test to create a new instance in database"""
    for customer in data:
        add_new_instance(*customer)
        logging.info ('Added test_new_instance')
    new_addition = Customer.get(Customer.customer_name == 'Aaa')
    assert new_addition.customer_ID == data[0][0]
    assert new_addition.customer_email == data[0][5]

def test_search_customer():
    ''' A test to search for existing customer in the database'''
    customer_id_list = []
    for customer in data:
        find_customer = Customer.get(Customer.customer_ID == customer[0])
        customer_id_list.append(find_customer.customer_ID)
    assert customer_id_list == [x[0] for x in data]
    test_dict = {}
    test_dict ['A0001'] = (data[0][1], data[0][2], data[0][5], data[0][4])
    assert test_dict == search_customer('A0001')

def test_del_customer():
    ''' Test to delete an existing customer'''
    delete_customer('A0001')
    assert search_customer('A0001') == {}
    assert search_customer('A0002') == {data[1][0] : (data[1][1], data[1][2], data[1][5], data[1][4])}

def test_update_credit():
    ''' Test to update the credit limit of the customer'''
    inti_credit = [x[-1] for x in data if x[0] == 'A0002']
    assert inti_credit != 100
    update_customer_credit('A0002', 100)
    query = Customer.get(Customer.customer_ID == 'A0002')
    assert query.customer_credit_limit != inti_credit
    assert query.customer_credit_limit == 100

def test_active_customers():
    ''' Test to determine number of active customers in the database'''
    count = 0
    for i in data:
        if i[6] == 'active':
            count += 1
    assert Customer.select().where(Customer.customer_status == 'active').count() == count

