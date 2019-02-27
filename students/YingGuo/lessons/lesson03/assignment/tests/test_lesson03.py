"""
pytest file for basic_operations.pytest
"""

from lesson03.assignment.basic_operations import *
from lesson03.assignment.management_database_model import *

import pytest

database.create_tables([Customer])

DICT_CUSTOMERS = {'002':["Lily", "Harmon", "Redmond WA", "111-111-1111", "Lily@gmail.com", True, 5000],
                    '003':["Jonathan", "Curtis", "Renton WA", "333-333-3333", 'Jon@gmail.com', False, 8888],
                    '004':["Tim", "Briest", "Seattle WA", "444-444-8888", 'tim@gmail.com', True, 6666]}

def test_add_customers():
    add_customers(DICT_CUSTOMERS)
    query = Customer.get(Customer.customer_id == '002')
    assert query.customer_name == 'Lily'

def test_update_customer_credit():
    update_customer_credit('003', 80000)
    query = Customer.get(Customer.customer_id == '003')
    assert query.credit_limit == 80000

def test_search_customer():
    a = search_customer("C000020")
    result = {"C000020": ["Wendy", "Schneider", "58859 Schmeler Wall", "(346)696-3257", "Randi@bridie.info", True, 249]}
    assert a == result

def test_delete_customer():
    delete_customer("123")
    assert search_customer("123") == {}

database.close()