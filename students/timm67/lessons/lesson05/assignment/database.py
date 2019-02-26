from pymongo import MongoClient


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='localhost', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

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
    pass


def show_rentals(product_id):
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
    pass


