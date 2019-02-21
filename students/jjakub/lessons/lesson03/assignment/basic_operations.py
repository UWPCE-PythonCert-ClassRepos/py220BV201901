# Basic Operation
# pylint: disable=unused-wildcard-import
# pylint: disable=too-many-arguments
# pylint: disable=wildcard-import
"""
Module to define the the basic operations
"""

from peewee import *
from create_database import *


def add_customer(customer_id, name, last_name, home_address, phone_number,
                 email_address, status, credit_limit):
    """ Add new customer to Customer table """
    with DATABASE.transaction():
        try:
            new_cust = Customer.create(
                customer_id=customer_id,
                name=name,
                last_name=last_name,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                status=status,
                credit_limit=credit_limit)
            new_cust.save()
        except IntegrityError:
            raise ValueError("Customer already exists")


def search_customer(customer_id):
    """ Search for customer in the Customer table """
    try:
        cust_dict = Customer.select().dicts().where(Customer.customer_id == customer_id)[0]
        return_dict = dict((key, value) for key, value in cust_dict.items()
                           if key in ('customer_id', 'name', 'last_name',
                                      'phone_number', 'email_address'))
    except IndexError:
        return_dict = {}
    return return_dict


def delete_customer(customer_id):
    """ Delete customer in the Customer table """
    remove_cust = Customer.delete().where(Customer.customer_id == customer_id)
    return remove_cust.execute()


def update_customer_credit(customer_id, credit_limit):
    """ Update a customers credit limit in Customer table """
    update_cust = Customer.update(credit_limit=credit_limit).where(Customer.customer_id ==
                                                                   customer_id)
    return update_cust.execute()


def list_active_customers():
    """ Count of all customers in Customer table with a status of Active """
    cust_cnt = Customer.select().where(Customer.status == 'Active').count()
    return cust_cnt
