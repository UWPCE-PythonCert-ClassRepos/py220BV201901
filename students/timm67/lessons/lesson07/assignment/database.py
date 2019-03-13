"""
mongodb database operations using mongoengnine
"""

from mongoengine import connect

from models import Customer
from models import Product
from models import Rental


class Connection:
    """
    Connection class to use as context manager for db connection
    """
    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = connect('mongoengine_test', host='localhost', port=27017)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


def show_available_products():
    """
    show_available_products(): Returns a Python dictionary of products
    listed as available with the following fields:
        product_id.
        description.
        product_type.
        quantity_available.

    For example:

    {‘prd001’:{‘description’:‘60-inch TV stand’,’product_type’:’livingroom’,
    ’quantity_available’:‘3’},’prd002’:{‘description’:’L-shaped sofa’,
    ’product_type’:’livingroom’,’quantity_available’:‘1’}}
    """
    ret_dict = {}

    with Connection():
        for prod in Product.objects:
            prod_entry = \
                {prod.product_id : {'description' : prod.description,
                                    'product_type' : prod.product_type,
                                    'quantity_available' : \
                                    prod.quantity_available}}
            ret_dict.update(prod_entry)

    return ret_dict


def show_rentals(prod_id):
    """
    Returns a Python dictionary with the following user information from users
    that have rented products matching product_id:

        user_id.
        name.
        address.
        phone_number.
        email.

    For example:

    {‘user001’:{‘name’:’Elisa Miles’,’address’:‘4490 Union Street’,
    ’phone_number’:‘206-922-0882’,’email’:’elisa.miles@yahoo.com’},
    ’user002’:{‘name’:’Maya Data’,’address’:‘4936 Elliot Avenue’,
    ’phone_number’:‘206-777-1927’,’email’:’mdata@uw.edu’}}
    """
    ret_dict = {}

    with Connection():
        renters = Rental.objects(product_id=prod_id)
        for renter in renters:
            users = Customer.objects(user_id=renter.user_id)
            for user in users:
                user_info = {user.user_id : {'name' : user.name,
                                             'address' : user.address,
                                             'phone_number' : user.phone_number,
                                             'email' : user.email
                                             }
                            }
                ret_dict.update(user_info)
    return ret_dict
