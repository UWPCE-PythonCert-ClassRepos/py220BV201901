"""
HP Norton operations for MongoDB
"""

import os
import logging
import time
from pathlib import Path
import pymongo


LOG_FORMAT = "%(asctime)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE_DB = 'db.log'
LOG_FILE_SYSTEM = 'system.log'

FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER_DB = logging.FileHandler(LOG_FILE_DB, mode='w')
FILE_HANDLER_DB.setFormatter(FORMATTER)

FILE_HANDLER_SYSTEM = logging.FileHandler(LOG_FILE_SYSTEM, mode='w')
FILE_HANDLER_SYSTEM.setFormatter(FORMATTER)

# Database access logging
DBLOG = logging.getLogger('DBLOG')
DBLOG.addHandler(FILE_HANDLER_DB)
DBLOG.setLevel("INFO")

# General logging
SYSTEMLOG = logging.getLogger('SYSTEMLOG')
SYSTEMLOG.addHandler(FILE_HANDLER_SYSTEM)
SYSTEMLOG.setLevel("INFO")

# MongoDB configurations
MYCLIENT = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
MYDB = MYCLIENT["HPNorton"]

PRODUCTCOLLECTION = MYDB["products"]
CUSTOMERCOLLECTION = MYDB["customers"]

MYDB.PRODUCTCOLLECTION.create_index('product_id', unique=True)
MYDB.CUSTOMERCOLLECTION.create_index('customer_id', unique=True)


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Writes file data to Mongo DB.
    example: <import_data(directory_name, product_file, customer_file, rentals_file)>

    :param: directory_name - location of files using forward slashes
    :param: product_file - comma separated file of products
    :param: customer_file - comma separated file of customers
    :param: rentals_file - comma separated file of rentals by customer
    """

    customersuccesscount, customerfailurecount = 0, 0
    productsuccesscount, productfailurecount = 0, 0
    rentalsuccesscount, rentalfailurecount = 0, 0

    starttime = time.time()

    # Process product file and add to mongoDB
    try:
        with open(Path(directory_name, product_file), 'r') as prodfile:

            next(prodfile) # skip header line
            for line in prodfile:
                linelist = [x.strip() for x in line.split(',')]

                try:
                    result = MYDB.PRODUCTCOLLECTION.insert_one(
                        {
                            'product_id' : linelist[0],
                            'description' : linelist[1],
                            'product_type' : linelist[2],
                            'quantity_available' : linelist[3]
                        })
                    if result.acknowledged:
                        productsuccesscount += 1
                    else:
                        productfailurecount += 1

                except pymongo.errors.DuplicateKeyError:
                    productfailurecount += 1
                    continue


                DBLOG.info(f'Added product DB entry: {linelist[0]}')

    except FileNotFoundError as fileerror:
        SYSTEMLOG.error(f'File not found at {directory_name + product_file}, exception {type(fileerror).__name__}')

    endtime = time.time()
    totaltime = endtime - starttime
    SYSTEMLOG.info(f'Add product operation time: {endtime - starttime}')

    starttime = time.time()

    # Process customer file and add to mongoDB
    try:
        with open(Path(directory_name, customer_file), 'r') as custfile:

            next(custfile) # skip header line
            for line in custfile:
                linelist = [x.strip() for x in line.split(',')]

                try:
                    result = MYDB.CUSTOMERCOLLECTION.insert_one(
                        {
                            'customer_id': linelist[0],
                            'name': linelist[1],
                            'last_name': linelist[2],
                            'address': linelist[3],
                            'phone_number': linelist[4],
                            'email': linelist[5],
                            'status': linelist[6],
                            'credit_limit': linelist[7]
                        })

                    if result.acknowledged:
                        customersuccesscount += 1
                    else:
                        customerfailurecount += 1

                except pymongo.errors.DuplicateKeyError:
                    customerfailurecount += 1
                    continue

                DBLOG.info(f'Added customer DB entry: {linelist[0]}')

    except FileNotFoundError as fileerror:
        SYSTEMLOG.error(f'File not found at {directory_name + product_file}, exception {type(fileerror).__name__}')

    endtime = time.time()
    totaltime += (endtime - starttime)
    SYSTEMLOG.info(f'Add customer operation time: {endtime - starttime}')

    starttime = time.time()

    # Process rental file and add to mongoDB in customer collection
    try:
        with open(Path(directory_name, rentals_file), 'r') as rentfile:

            next(rentfile) # skip header line
            for line in rentfile:
                linelist = [x.strip() for x in line.split(',')]

                try:
                    result = MYDB.RENTALCOLLECTION.insert_one(
                        {
                            'user_id': linelist[0],
                            'name': linelist[1],
                            'address': linelist[2],
                            'phone_number': linelist[3],
                            'email': linelist[4],
                            'product_id': linelist[5]
                        })
                    if result.acknowledged:
                        rentalsuccesscount += 1
                    else:
                        rentalfailurecount += 1

                except pymongo.errors.DuplicateKeyError:
                    rentalfailurecount += 1
                    continue

                DBLOG.info(f'Added rental DB entry to customer: {linelist[1]}')

    except FileNotFoundError as fileerror:
        SYSTEMLOG.error(f'File not found at {directory_name + product_file}, exception {type(fileerror).__name__}')

    endtime = time.time()
    SYSTEMLOG.info(f'Add rental operation time: {endtime - starttime}')

    totaltime += (endtime - starttime)
    SYSTEMLOG.info(f'Full add and update time: {totaltime}')

    return (productsuccesscount, customersuccesscount, rentalsuccesscount), (productfailurecount, customerfailurecount, rentalfailurecount)


def show_available_products():
    """ Returns all products with quantity greater than 0 """

    result = {}

    for document in MYDB.PRODUCTCOLLECTION.find({"quantity_available": {"$gt": "0"}}):
        key = document['product_id']

        result[key] = {
            'description': document['description'],
            'product_type': document['product_type'],
            'quantity_available': document['quantity_available']
            }

    return result


def show_rentals(productid):
    """
    Returns dictionary of customers with the provided
    product_id in the rentals field.

    :param: product id rented by a customer
    """

    result = {}

    for rental in MYDB.RENTALCOLLECTION.find({"product_id": {"$eq": productid}}):

        result[rental['user_id']] = {
            'name': rental['name'],
            'address': rental['address'],
            'phone_number': rental['phone_number'],
            'email': rental['email']
            }

    return result


if __name__ == "__main__":

    directory = os.path.dirname(os.path.abspath(__file__))
    resultgood, resultfail = import_data(directory, 'products.csv', 'customers.csv', 'rentals.csv')

    SYSTEMLOG.info(f"Success counts: {resultgood}  Failed counts: {resultfail}")
