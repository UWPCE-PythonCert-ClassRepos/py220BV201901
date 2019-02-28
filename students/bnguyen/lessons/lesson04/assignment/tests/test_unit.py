# Student: Bradnon Nguyen
# Class:   Advance Python 220 - Jan2019
# Lesson03/04 - test_unit.py : 
"""Basic Unit test of model and other operation"""

# from unittest import TestCase

import pytest
import peewee

from unittest.mock import MagicMock
from lesson04.assignment.customer_db_model import *
from lesson04.assignment import basic_operations as bo
from lesson04.assignment.basic_operations import LOGGER


# class CustomerModelTests(TestCase):
#     """
#     Basic tests for the customers db model.
#     """
#     pass

# class BasicOperationsTests(TestCase):
#     """
#     Basic tests the add,delete...operation.
#     """
#     pass

bo.initialize_db(CustomerA)  # get the DB.


@pytest.fixture
def _add_customers_positive_data():
    """Data set up.  Return a list of customers to add for positive tests."""
    return [
        ("123", "Name", "Lastname", "Address", "phone", "email", "active", 999),
        ("456", "Name", "Lastname", "Address", "phone", "email", "inactive", 10),
    ]


@pytest.fixture
def _add_customers_negative_data():
    """Data set up.  Return a list of customers to add for negative tests."""
    return [
        ("235", "Name", "Lastname", "Address", "phone", "email", "active", 0),
        ("678", "Name", "Lastname", "Address", "phone", "email", "iinactive", 10),
    ]


def test_add_customer_a_model(_add_customers_positive_data):
    """ Test additions for model customer A """
    
    DB.connect(reuse_if_open=True)
    DB.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only
    for customer in _add_customers_positive_data:
        with DB.transaction():
            new_customer = CustomerA.create(
                customer_id=customer[0],
                name=customer[1],
                lastname=customer[2],
                home_address=customer[3],
                phone_number=customer[4],
                email=customer[5],
                status=customer[6],
                credit_limit=customer[7]
            )
            new_customer.save()
        added = CustomerA.get(CustomerA.customer_id == customer[0])
        assert added.name == customer[1]
        assert added.lastname == customer[2]
        assert added.email == customer[5]
        assert added.credit_limit == customer[7]

    # Exit criteria is to clean up clear DB model before next test
    for customer in _add_customers_positive_data:
        customer_tb_rm = CustomerA.get(CustomerA.customer_id == customer[0])
        customer_tb_rm.delete_instance()

    search_returned = CustomerA.select().where(CustomerA.status == 'active' or
                                               CustomerA.status == 'inactive').count()
    assert search_returned == 0  # make sure there is no longer a record

    DB.close()


# def test_add_customer_a_model_fail(_add_customers_negative_data):
#     """ Test additions for model customer A """
    
#     DB.connect(reuse_if_open=True)
#     DB.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only
#     for customer in _add_customers_negative_data:
#         with DB.transaction():
#             new_customer = CustomerA.create(
#                 customer_id=customer[0],
#                 name=customer[1],
#                 lastname=customer[2],
#                 home_address=customer[3],
#                 phone_number=customer[4],
#                 email=customer[5],
#                 status=customer[6],
#                 credit_limit=customer[7]
#             )
#             new_customer.save()
#         added = CustomerA.get(CustomerA.customer_id == customer[0])
#         assert added.name == customer[1]
#         assert added.lastname == customer[2]
#         assert added.email == customer[5]
#         assert added.credit_limit == customer[7]

#     # Exit criteria is to clean up clear DB model before next test
#     for customer in _add_customers_negative_data:
#         customer_tb_rm = CustomerA.get(CustomerA.customer_id == customer[0])
#         customer_tb_rm.delete_instance()

#     search_returned = CustomerA.select().where(CustomerA.status == 'active' or
#                                                CustomerA.status == 'inactive').count()
#     assert search_returned == 0  # make sure there is no longer a record

#     DB.close()

def test_add_customers_with_csv():
    list_data = bo.process_csv("customer2.csv")
    bo.add_customers(list_data)
    # C000386 Kamryn
    search = bo.search_customer('C000386')
    LOGGER.warning(f'TEST: {search["name"]}')
    assert search["name"] == "Kamryn"