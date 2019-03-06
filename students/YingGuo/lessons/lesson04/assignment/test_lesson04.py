"""
test file
"""

import pytest

from lesson04.assignment.basic_operations import *

def test_add_many_customers():
    list_customers = [
        ["123", "Name", "Lastname", "Address", "phone", "email", "active", 999],
        ["456", "Name", "Lastname", "Address", "phone", "email", "inactive", 10]
    ]
    add_many_customers(list_customers)
    print(search_customer("123"))
    print(search_customer("456"))
    assert search_customer("456") == {"123": ["Name", "Lastname", "Address", "phone", "email", False, 10]}

def test_search_customer():
    a = search_customer("C000020")
    result = {"C000020": ["Wendy", "Schneider", "58859 Schmeler Wall", "(346)696-3257", "Randi@bridie.info", True, 249]}
    assert a == result

def test_delete_customer():
    delete_customer("123")
    assert search_customer("123") == {}

def test_update_customer_credit():
    update_customer_credit("C000021", 800)
    a = search_customer("C000021")
    new_credit = a["C000021"][-1]
    assert new_credit == 800
