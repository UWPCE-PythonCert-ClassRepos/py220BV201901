# Student: Bradnon Nguyen
# Class:   Advance Python 220 - Jan2019
# Lesson07 - mongodb database.py.
"""
This module is modified from database.py in lesson 5 to become linear.py
"""
import logging
import datetime
import time
import csv
import os
import pprint
from pymongo import MongoClient


# LOGGING SETTING START
LOG_FORMAT = "%(asctime)s %(filename)s:%(funcName)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d")+'db.log'
FORMATTER = logging.Formatter(LOG_FORMAT)

# Log setting for writing to file
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.WARNING)  # Saving to log file via level
FILE_HANDLER.setFormatter(FORMATTER)

# Log setting for display to standout.
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)  # Send log to console: DEBUG level
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)
# LOGGING SETTING END!
# ALL dblog is writing into file via WARNING level change it to turn off.


class MongoDBConnection():
    """
    This is a context manager for MongoDB.  It has methods to connect and disconnect to db.
    """
    def __init__(self, host='127.0.0.1', port=27017):
        """This is a connection string.  CAUTION: not for production"""
        # look into production connection string
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """Conection method, use to connect to db."""
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """This is used to close out the context manager by closing connection to db."""
        self.connection.close()


def print_mdb_collection(collection_name):
    """
    This bare bone function should be used within a context conn manager.
    Purpose: to print out row in a table.
    """
    pp = pprint.PrettyPrinter(indent=4, width=100)

    for doc in collection_name.find({}):
        pp.pprint(doc)


def process_csv_basic(csv_file_in):
    """
    This function is to read in csv data and return a list of dictionaries.
    """
    data = []

    with open(csv_file_in, 'r', encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # assuming that csv has header row.
        try:
            for row in map(dict, reader):
                LOGGER.warning(f'CSV: processing the the next row: {row}.')
                data.append(row)  # adding the data row into list data
        except csv.Error as errs:
            LOGGER.error(f"Some sort of data process issue: {row}")
            LOGGER.error(errs)

    LOGGER.warning(f'FULLDICT{data}.')

    return data


def update_db(collection_name, dir_name, file_name, key_name=None, key_name_1=None):
    """
    This function is to update mongodb.
    Params: collection_name, dir_name, file_name, key_name=None, key_name_1=None.
    All params are string.  the key_names are for us to set the Index.
    Return: a list of tuples.
    Each tuple will contain 4 values: the number of records processed,
    the record count in the database prior to running, the record count
    after running, and the time taken to run the module.
    """

    start_time = time.time()

    file_path_name = os.path.join(dir_name, file_name)
    csv_list = process_csv_basic(file_path_name)

    # TODO working here NOW
    # adds, errors = 0, 0
    processed_cnt, count_collection_pre, count_collection_post = 0, 0, 0

    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.hp_inventory  # hp_inventory is db name.
        table_name = db[collection_name]
        count_collection_pre = table_name.count_documents({}) # due to drop collection will be 0
        # NEED help - with unique constrain on key
        if key_name is not None:
            table_name.create_index(key_name, unique=True)
        elif key_name is not None and key_name_1 is not None:
            table_name.create_index(key_name, key_name_1, unique=True)
        try:
            for row in csv_list:
                result = table_name.insert_one(row)
                LOGGER.warning(f'{collection_name.upper()}: insert is ok. {result}:{row}')
                processed_cnt += 1
        except Exception as errs:
            LOGGER.error(f'{collection_name.upper()}_FAIL: Something wrong. {errs}')
            # errors += 1  # From lesson 5 not needed here.
        count_collection_post = table_name.count_documents({})

    end_time = time.time()

    return processed_cnt, count_collection_pre, count_collection_post, end_time - start_time


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    This function takes a directory name three csv files as input:
    one with product data, one with customer data and the third one with rentals data
    and creates and populates a new MongoDB database with the these data.
    params: directory_name, product_file, customer_file, rentals_file.
    returns 3 tuples:
    - Each for products, customers, and rental - with a process_record, collection_count_before, collection count after 
    products, customers and rentals added (in that order).
    
    """

    products_processed_cnt, products_pre_cnt, products_post_cnt, prod_time = 0, 0, 0, 0.0
    customers_processed_cnt, customers_pre_cnt, customers_post_cnt, cust_time = 0, 0, 0, 0.0
    rentals_processed_cnt, rentals_pre_cnt, rentals_post_cnt, rent_time = 0, 0, 0, 0.0


    products_processed_cnt, products_pre_cnt, products_post_cnt, prod_time = update_db('products', 
                                                                                        directory_name, 
                                                                                        product_file, 
                                                                                        'product_id')
    customers_processed_cnt, customers_pre_cnt, customers_post_cnt, cust_time = update_db('customers', directory_name,
                                                                                         customer_file, 'Id')
    # I believe that rental csv should have rental_id to record the unique transaction
    rentals_processed_cnt, rentals_pre_cnt, rentals_post_cnt, rent_time = update_db('rentals', directory_name,
                                           rentals_file, 'user_id', 'product_id')

    return ((products_processed_cnt, products_pre_cnt, products_post_cnt, prod_time),
            (customers_processed_cnt, customers_pre_cnt, customers_post_cnt, cust_time),
            (rentals_processed_cnt, rentals_pre_cnt, rentals_post_cnt, rent_time))


def drop_db(input_val=None):
    """
    This function is used to drop all the collections.
    Param: input_val is a string "y", or "n"
    """
    # start afresh next time?
    mongo_conn = MongoDBConnection()

    with mongo_conn:
        # mongodb database; it all starts here
        db = mongo_conn.connection.hp_inventory

        if input_val is None:
            yorn = input("Drop data?")
        else:
            yorn = input_val
        if yorn.upper() == 'Y':
            db.drop_collection("customers")
            db.drop_collection("products")
            db.drop_collection("rentals")


def main():
    """ This is just main. """

    drop_db("y")

    dir_a = '/Users/bnguyen/py220BV201901/students/bnguyen/lessons/lesson07/assignment/tests/'
    # data_dir = os.path.dirname(os.path.abspath(dir_a))
    data_dir = os.path.abspath(os.path.dirname(dir_a))
    products, customers, rentals = import_data(data_dir, 'products.csv', 'customers.csv', 'rentals.csv')

    print()
    print(products, customers, rentals)

    drop_db()

if __name__ == "__main__":
    main()
