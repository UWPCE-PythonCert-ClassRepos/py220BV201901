'''
Yushu Song
Assignment 05
'''

import csv
import datetime
import os
import logging
from pymongo import MongoClient

LOGGER = logging.getLogger()
HANDLER = logging.StreamHandler()
FORMATTER = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)
LOGGER.setLevel(logging.INFO)

class MongoDBConnection(object):
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """
        be sure to use the ip address not name for local windows
        CAUTION: Don't do this in production!!!
        """
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """
        Setup connection to mongoDB
        """
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the connection
        """
        self.connection.close()

def import_data(directory_name, product_file, customer_file, rentals_file):
    '''
    Read in product, customer, and rental files and populate mongo db collections
    '''
    mongo = MongoDBConnection()
    with mongo:
        # mongodb database; it all starts here
        db = mongo.connection.inventory
        # initialize collection and error count
        product_added, customer_added, rental_added = 0, 0, 0
        product_error, customer_error, rental_error = 0, 0, 0

        try:
            # process products data
            with open(os.path.join(directory_name, product_file),
                      encoding='utf-8-sig',
                      newline='') as prod_file:

                # add customer collection
                prod_data = csv.DictReader(prod_file)
                prod_col = db["products"]

                for row in prod_data:
                    quantity = int(row["quantity_available"])
                    prod_col.insert_one({"product_id":row["product_id"],
                                         "description":row["description"],
                                         "product_type":row["product_type"],
                                         "quantity_available":quantity})
                    product_added += 1

        except Exception as ex:
            product_error += 1
            LOGGER.error(ex)

        try:
            # process customers data
            with open(os.path.join(directory_name, customer_file),
                      encoding='utf-8-sig',
                      newline='') as csvfile:

                # add customer collection
                customer_data = csv.DictReader(csvfile)
                customer_col = db["customers"]
                for row in customer_data:
                    customer_col.insert_one(row)
                    customer_added += 1

        except Exception as ex:
            customer_error += 1
            LOGGER.error(ex)

        try:
            # process rentals data
            with open(os.path.join(directory_name, rentals_file),
                      encoding='utf-8-sig',
                      newline='') as rent_file:

                # add customer collection
                rent_data = csv.DictReader(rent_file)
                rent_col = db["rentals"]
                for rent in rent_data:
                    rent_col.insert_one(rent)
                    rental_added += 1

        except Exception as ex:
            rental_error += 1
            LOGGER.error(ex)

    return ((product_added, customer_added, rental_added),
            (product_error, customer_error, rental_error))

def show_available_products():
    '''
    Show all the products available to rent
    '''
    mongo = MongoDBConnection()
    with mongo:
        mongo_db = mongo.connection.inventory
        prod_col = mongo_db["products"]
        products = {}

        for product in prod_col.find({"quantity_available": {"$gt": 0}}):
            products[product["product_id"]] = {"description":product["description"],
                                               "product_type":product["product_type"],
                                               "quantity_available":product["quantity_available"]}
        return products

def show_rentals(product_id):
    '''
    Given a product id find all the users who made a rental
    '''
    mongo = MongoDBConnection()
    with mongo:
        mongo_db = mongo.connection.inventory
        customer_col = mongo_db["customers"]
        rental_col = mongo_db["rentals"]
        users = {}

        for rent in rental_col.find({"product_id": product_id}):
            user_id = rent["user_id"]
            customer = customer_col.find_one({"user_id": user_id})
            users[user_id] = {"name":customer["name"],
                              "address":customer["address"],
                              "phone_number":customer["phone_number"],
                              "email":customer["email"]}
    return users

def print_dict(data):
    '''
    Print items in a dictionary
    '''
    for key, value in data.items():
        print(f"{key}: {value}")

def main():
    '''
    Define main flow
    '''
    start = datetime.datetime.now()
    added, errors = import_data(os.path.dirname(os.path.abspath(__file__)),
                                'products.csv',
                                'customers.csv',
                                'rentals.csv')
    products = show_available_products()
    end = datetime.datetime.now()
    user_data = show_rentals("prd005")
    print_dict(products)
    print_dict(user_data)
    print(added)
    print(errors)
    print(end-start)

if __name__ == "__main__":
    main()
