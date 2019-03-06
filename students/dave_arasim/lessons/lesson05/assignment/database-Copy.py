""""
MongoDB database model for Lesson 5
"""

import os
from pymongo import MongoClient


class MongoDBConnection(object):
    """ MongoDB Connection for content manager """

    def __init__(self, host='127.0.0.1', port=27017):
        """ Use the ip address and specific port for local windows """

        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def print_mdb_collection(collection_name):
    """ Print out the particular MongoDB database collection """
    mongo = MongoDBConnection()

    with mongo:
        # mongodb database defined
        db = mongo.connection.media

        # collections in the MongoDB database
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        for doc in collection_name.find():
            print(doc)


def show_available_products():
    out_doc = {}

    mongo = MongoDBConnection()

    with mongo:
        # mongodb database defined
        db = mongo.connection.media

        # collections in the MongoDB database
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        for doc in products.find():
            out_doc[doc['product_id']] = {
                'description' : doc['description'],
                'product_type' : doc['product_type'],
                'quantity_available' : doc['quantity_available']
            }

    return out_doc


def show_rentals(search_product_id):
    out_doc = {}

    mongo = MongoDBConnection()

    with mongo:
        # mongodb database defined
        db = mongo.connection.media

        # collections in the MongoDB database
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        for doc in rentals.find():
            if doc['product_id'] == search_product_id:
                out_doc[doc['user_id']] = {
                    'name' : doc['name'],
                    'address' : doc['address'],
                    'phone_number' : doc['phone_number'],
                    'email' : doc['email']
                }

    return out_doc


def import_data(data_dir, products_file, customers_file, rentals_file):
    mongo = MongoDBConnection()

    with mongo:
        # mongodb database defined
        db = mongo.connection.media

        # collections in the MongoDB database
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        # Insert Products file records
        add_prod = 0
        err_prod = 0

        try:
            with open(data_dir + "\\" + products_file, 'r') as csv_file:
                csv_header = csv_file.readline()

                while csv_header:
                    csv_line = csv_file.readline()
                    if not csv_line: break

                    data_in = dict(zip(csv_header.strip().split(','), csv_line.strip().split(',')))

                    try:
                        products.insert_one(data_in)
                        add_prod += 1
                    except:
                        print(f'failed to insert: {data_in}\n')
                        err_prod += 1

            csv_file.close()

        except FileNotFoundError:
            print('File not found: ', data_dir + "\\" + products_file)

        # Insert Customers file records
        add_cust = 0
        err_cust = 0

        try:
            with open(data_dir + "\\" + customers_file, 'r') as csv_file:
                csv_header = csv_file.readline()

                while csv_header:
                    csv_line = csv_file.readline()
                    if not csv_line: break

                    data_in = dict(zip(csv_header.strip().split(','), csv_line.strip().split(',')))

                    try:
                        customers.insert_one(data_in)
                        add_cust += 1
                    except:
                        print(f'failed to insert: {data_in}\n')
                        err_cust += 1

            csv_file.close()

        except FileNotFoundError:
            print('File not found: ', data_dir + "\\" + customers_file)

        # Insert Rentals file records
        add_rent = 0
        err_rent = 0

        try:
            with open(data_dir + "\\" + rentals_file, 'r') as csv_file:
                csv_header = csv_file.readline()

                while csv_header:
                    csv_line = csv_file.readline()
                    if not csv_line: break

                    data_in = dict(zip(csv_header.strip().split(','), csv_line.strip().split(',')))

                    try:
                        rentals.insert_one(data_in)
                        add_rent += 1
                    except:
                        print(f'failed to insert: {data_in}\n')
                        err_rent += 1

            csv_file.close()

        except FileNotFoundError:
            print('File not found: ', data_dir + "\\" + rentals_file)

    added = (add_prod, add_cust, add_rent)
    errors = (err_prod, err_cust, err_rent)

    return added, errors


def drop_data():
    mongo = MongoDBConnection()

    with mongo:
        # mongodb database defined
        db = mongo.connection.media

        # collections in the MongoDB database
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]
        
        products.drop()
        customers.drop()
        rentals.drop()


def main():
    mongo = MongoDBConnection()

    with mongo:
        # mongodb database defined
        db = mongo.connection.media

        # collections in the MongoDB database
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        data_dir = os.path.dirname(os.path.abspath(__file__))
        added, errors = import_data(data_dir, "product.csv", "customer.csv", "rental.csv")

        print(f'Added records: {added}\n')
        print(f'Error records: {errors}\n')

        print('Products:')
        print_mdb_collection(products)
        print()
        print()
        print('Customers:')
        print_mdb_collection(customers)
        print()
        print()
        print('Rentals:')
        print_mdb_collection(rentals)
        print()
        print()

        print ('show_available_products output:')
        print(show_available_products())
        print()
        print()

        print ('show_rentals output for P000003:')
        print(show_rentals('P000003'))
        print()
        print()
        
        # Option to drop data from collections
        yorn = input("Drop data?")

        if yorn.upper() == 'Y':
            drop_data()


if __name__== "__main__":
    main()
