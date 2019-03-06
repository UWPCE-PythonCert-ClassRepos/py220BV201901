# Basic Operation
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
"""
Module to define the the basic operations
"""

from peewee import *
from create_database import *


def add_customer(customer_id, name, lastname, address, phone_number,
                 email, status, credit_limit):
    """ Add new customer to customer table """
    with DATABASE.transaction():
        try:
            new_cust = Customer.create(
                customer_id=customer_id,
                name=name,
                lastname=lastname,
                address=address,
                phone_number=phone_number,
                email=email,
                status=status,
                credit_limit=credit_limit)
            new_cust.save()
        except IntegrityError:
            print(f"Customer ID {customer_id} already exists")
        except ValueError:
            print(f"Customer ID {customer_id} has invalid data type")


def search_customer(customer_id):
    """ Search for customer in the Customer table """
    try:
        search_id = Customer.get(Customer.customer_id == customer_id)
        print(f"Customer ID {customer_id} found")

        cust_dict = {"name": search_id.name, "lastname": search_id.lastname,
                     "email": search_id.email, "phone_number": search_id.phone_number}
        return cust_dict
    except DoesNotExist:
        print(f"Customer ID {customer_id} not found")
        return {}


def delete_customer(customer_id):
    """ Delete customer in the Customer table """
    try:
        remove_cust = Customer.get(Customer.customer_id == customer_id)
        remove_cust.delete_instance()
        print(f"Customer ID {customer_id} deleted")
        return True
    except DoesNotExist:
        print(f"Customer ID {customer_id} not found")
    except OperationalError:
        print(f"Customer ID {customer_id} not found")


def update_customer_credit(customer_id, credit_limit):
    """ Update a customers credit limit in Customer table """
    try:
        Customer.get(Customer.customer_id == customer_id)
        update_cust = Customer.update(credit_limit=credit_limit).where(Customer.customer_id ==
                                                                       customer_id)
        print(f"Credit limit for Customer ID {customer_id} updated to {credit_limit}")
        update_cust.execute()
    except DoesNotExist:
        print(f"Customer ID {customer_id} not found")
        raise ValueError('NoCustomer')


def list_active_customers():
    """ Count of all customers in Customer table with a status of Active """
    cust_cnt = Customer.select().where(Customer.status == 'active'
                                       or Customer.status == 'Active').count()
    print(f"There are {cust_cnt} active customers in the table")
    return cust_cnt


def list_all_customers():
    """ Count of all customers in Customer table """
    cust_cnt = Customer.select().count()
    print(f"There are {cust_cnt} customers in the table")
    return cust_cnt

if __name__ == "__main__":
    main()
