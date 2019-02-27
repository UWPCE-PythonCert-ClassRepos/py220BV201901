"""test file for database.py"""

from lesson05.assignment.database import *
import pytest

def test_products_to_db_and_show_available_products():
    """
    test products_to_db function
    and show_available_products
    """
    products_to_db("products", "products")
    op = show_available_products()
    expectation = {'description': '60-inch TV stand', 'product_type': 'livingroom', 'quantity_available': '3'}
    assert op['prd001'] == expectation

def test_show_rentals():
    """
    test:
    show_rentals function
    rentals_to_db function
    customers_to_db function
    """
    rentals_to_db("rentals", "rentals")
    customer_to_db("customers","customers")
    op = show_rentals()
    expectation = {'name': 'Flor Matatena', 'address': '885 Boone Crockett Lane', 'phone_number': '206-414-2629', 
    'email': 'matseattle@pge.com'}
    assert op['user004'] == expectation