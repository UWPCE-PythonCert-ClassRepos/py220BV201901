#!/usr/bin/env python3

"""
based on lesson05 MongoDB assignment.
This is linear version compared to parallel version.

This module will return a list of tuples, one tuple for customer and one for products.
Each tuple will contain 4 values: 
the number of records processed (int), 
the record count in the database prior to running (int),
the record count after running (int),
and the time taken to run the module (float).
"""

from pymongo import MongoClient
import csv
import logging
import datetime

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def customer_to_db(file_name, db_collection):
    """
    This function write csv file into database
    example at customers.csv
    user_id,name,address,zip_code,phone_number,email
    """
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.inventory
        db_collection = db[db_collection]

        fh = open("{}.csv".format(file_name))
        reader = csv.reader(fh)
        line = 0
        for row in reader:
            line += 1
            if line == 1:
                continue
            row_ip = {"user_id":row[0],
                        "name":row[1],
                        "address":row[2],
                        "zip_code":row[3],
                        "phone_number":row[4],
                        "email":row[5]}
            result = db_collection.insert_one(row_ip)
            logging.info(f"{row} is imported to database collection customers")
        fh.close()

def products_to_db(file_name, db_collection):
    """
    This function write csv file into database
    example at products.csv
    product_id,description,product_type,quantity_available
    """
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.inventory
        db_collection = db[db_collection]

        fh = open("{}.csv".format(file_name))
        reader = csv.reader(fh)
        line = 0
        for row in reader:
            line += 1
            if line == 1:
                continue
            row_ip = {"product_id":row[0],
                        "description":row[1],
                        "product_type":row[2],
                        "quantity_available":row[3]
                        }
            result = db_collection.insert_one(row_ip)
            logging.info(f"{row} is imported to database collection products")
        fh.close()

def count_records_csv(file_name):
    fh = open("{}.csv".format(file_name))
    reader = csv.reader(fh)
    count = -1
    for row in reader:
        count += 1
    return count

def count_records_db(collection_name):
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.inventory
        collect = db[collection_name]
        count = 0
        for record in collect.find():
            count += 1
    return count


if __name__ == "__main__":
    customer_csv_count = count_records_csv("customers")
    product_csv_count = count_records_csv("products")

    beginning_db_customers_count = count_records_db("customers")
    beginning_db_products_count = count_records_db("products")

    start = datetime.datetime.now()
    mongo = MongoDBConnection()
    customer_to_db("customers", "customers")
    products_to_db("products", "products")
    end = datetime.datetime.now()
    d = end - start
    duration = d.total_seconds()

    end_db_customers_count = count_records_db("customers")
    end_db_products_count = count_records_db("products")

    # the number of records processed (int), 
    # the record count in the database prior to running (int),
    # the record count after running (int),
    # and the time taken to run the module (float)
    tuple_customers = (customer_csv_count, beginning_db_customers_count, end_db_customers_count, duration)
    tuple_products = (product_csv_count, beginning_db_products_count, end_db_products_count, duration)
    print(f"customer collection tuple:{tuple_customers}")
    print(f"product collection tuple:{tuple_products}")

    #clean database
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.inventory
        customers = db["customers"]
        products = db["products"]
        rentals = db["rentals"]

        yorn = input("Drop data?")
        if yorn.upper() == 'Y':
            customers.drop()
            rentals.drop()
            products.drop()