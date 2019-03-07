# Student: Bradnon Nguyen
# Class:   Advance Python 220 - Jan2019
# Lesson05 - mongodb database.py.
"""
This module is used for creating collection for mongoDB.
"""
import logging
import datetime
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


def process_csv(csv_file_in, key_name):
    """
    Read in csv file and return a list of rows in dict.
    Params: csv file name, key_name (string).
    Return: a Dict and 2 counters added and errors.
    Error here resulted from key alreay exist checked.
    """
    data = {}
    added = 0
    errors = 0

    with open(csv_file_in, 'r', encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # assuming that csv has header row.
        try:
            for row in map(dict, reader):
                LOGGER.warning(f'CSV: processing the the next row: {row}.')
                val = row.pop(key_name)  # remove & return the key_name's val as a key
                # Cheap way to detect key errors
                if val not in data.keys():
                    data[val] = row
                    added += 1
                    LOGGER.warning(f'DICT: processing the next row: {val}:{data[val]}.')
                else:
                    errors += 1
                    LOGGER.warning(f'DICT: skip processing this row: {val}:{data[val]}.')
        except csv.Error as errs:
            LOGGER.error(f"Some sort of data process issue: {row}")
            LOGGER.error(errs)

    LOGGER.warning(f'FULLDICT{data}.')
    LOGGER.warning(f'COUNT: added = {added}. Errors = {errors}.')

    return data, added, errors


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
    Returns the adds and errors value for the collection passed in.
    """

    file_path_name = os.path.join(dir_name, file_name)
    csv_list = process_csv_basic(file_path_name)

    adds, errors = 0, 0

    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.hp_inventory  # hp_inventory is db name.
        table_name = db[collection_name]
        # NEED help - with unique constrain on key
        if key_name is not None:
            table_name.create_index(key_name, unique=True)
        elif key_name is not None and key_name_1 is not None:
            table_name.create_index(key_name, key_name_1, unique=True)
        try:
            for row in csv_list:
                result = table_name.insert_one(row)
                LOGGER.warning(f'{collection_name.upper()}: insert is ok. {result}:{row}')
                adds += 1
        except Exception as errs:
            LOGGER.error(f'{collection_name.upper()}_FAIL: Something wrong. {errs}')
            errors += 1

    return adds, errors


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    This function takes a directory name three csv files as input:
    one with product data, one with customer data and the third one with rentals data
    and creates and populates a new MongoDB database with the these data.
    params: directory_name, product_file, customer_file, rentals_file.
    returns 2 tuples:
    - The first - with a record count of the number of
    products, customers and rentals added (in that order).
    - The second with a count of any errors that occurred, in the same order.
    """

    product_adds, customer_adds, rental_adds = 0, 0, 0
    product_errors, customer_errors, rental_errors = 0, 0, 0

    product_adds, product_errors = update_db('products', directory_name,
                                             product_file, 'product_id')
    customer_adds, customer_errors = update_db('customers', directory_name,
                                               customer_file, 'Id')
    # I believe that rental csv should have rental_id to record the unique transaction
    rental_adds, rental_errors = update_db('rentals', directory_name,
                                           rentals_file, 'user_id', 'product_id')

    return ((product_adds, customer_adds, rental_adds),
            (product_errors, customer_errors, rental_errors))


def show_distinct_products():
    """
    This function is resulted of a misread requirement.  Save for later other refractor need.
    Currently it returns all distinct documents in collection products.
    """
    data = {}
    mongo_conn = MongoDBConnection()

    with mongo_conn:
        # mongodb database; it all starts here
        db = mongo_conn.connection.hp_inventory
        product_collection = db["products"]

        this_data = product_collection.distinct("product_id") # prevents duplication ?
        for val in this_data:
            for product in product_collection.find({"product_id": val}):
                data[product["product_id"]] = {"description": product["description"],
                                               "product_type": product["product_type"],
                                               "quantity_available": product["quantity_available"]}
    return data


def show_available_products():
    """
    Returns a Python dictionary of products listed as available with the following fields:
    product_id. description. product_type. quantity_available.
    *Criteria: Quanity > 0
    """
    # db.inventory.find( { qty: { '$gt': '20' } } )  # The quote is key!
    data = {}
    mongo_conn = MongoDBConnection()
    with mongo_conn:
        db = mongo_conn.connection.hp_inventory
        product_collection = db["products"]
        try:
            for product in product_collection.find({"quantity_available": {'$gt': '0'}}):
                data[product["product_id"]] = {"description": product["description"],
                                               "product_type": product["product_type"],
                                               "quantity_available": product["quantity_available"]}
        except Exception as errs:
            LOGGER.info(f'SHOW_PRODUCT: something wrong : {errs}')

    return data


def show_rentals(product_id):
    """
    Returns a Python dictionary with the following user information
    from users that have rented products matching product_id:
    user_id. name. address. phone_number. email.
    """
    data = {}
    mongo_conn = MongoDBConnection()

    with mongo_conn:
        # mongodb database; it all starts here
        db = mongo_conn.connection.hp_inventory
        table_name = db["rentals"]

        for rental in table_name.find({"product_id": product_id}):
            data[rental["user_id"]] = {"name": rental["name"],
                                       "address": rental["address"],
                                       "phone_number": rental["phone_number"],
                                       "email": rental["email"]}

    return data


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
    dir_a = '/Users/bnguyen/py220BV201901/students/bnguyen/lessons/lesson05/assignment/tests/'
    # data_dir = os.path.dirname(os.path.abspath(dir_a))
    data_dir = os.path.abspath(os.path.dirname(dir_a))
    added, errs = import_data(data_dir, 'product.csv', 'customer.csv', 'rental.csv')

    print()
    print(added, errs)

    mongo_conn = MongoDBConnection()

    with mongo_conn:
        # mongodb database; it all starts here
        db = mongo_conn.connection.hp_inventory
        product_colection = db["products"]
        customer_collection = db["customers"]
        rental_collection = db["rentals"]

    pp = pprint.PrettyPrinter(indent=4, width=100)
    print("Available products are:\n")
    pp.pprint(show_available_products())

    print("\n\n Rental record with P000001 are:")
    pp.pprint(show_rentals("P000001"))

    prod_cnt = product_colection.count_documents({})
    cus_cnt = customer_collection.count_documents({})
    rent_cnt = rental_collection.count_documents({})

    print(f"\nCurrent prod_count: {prod_cnt}| cust_cnt: {cus_cnt}| rent_cnt: {rent_cnt}")

    drop_db()

if __name__ == "__main__":
    main()
