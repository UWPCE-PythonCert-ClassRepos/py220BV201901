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
    assert search_customer("123") == {"123": ["Name", "Lastname", "Address", "phone", "email", "active", 999]}

def test_search_customer():
    a = search_customer("C000020")
    result = {"C000020": ["Taylor", "Bradtke", "451", "Gerhold Burgs", "597.487.6813", "Brando.Barton@wilford.com", True, 474]}
    assert a == result
