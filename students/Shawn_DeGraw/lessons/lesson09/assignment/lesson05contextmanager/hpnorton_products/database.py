"""
HP Norton operations for MongoDB
"""

import logging
from pathlib import Path
from pymongo import MongoClient, errors


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


class MongoDBConnection:
    """ MongoDB Connection manager """

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        DBLOG.info('Opening connection to MongoDB.')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        DBLOG.info('Closing connection to MongoDB.')
        self.connection.close()


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Writes file data to Mongo DB.
    example: <import_data(directory_name, product_file, customer_file, rentals_file)>

    :param: directory_name - location of files using forward slashes
    :param: product_file - comma separated file of products
    :param: customer_file - comma separated file of customers
    :param: rentals_file - comma separated file of rentals by customer
    """

    mongo = MongoDBConnection()

    customersuccesscount, customerfailurecount = 0, 0
    productsuccesscount, productfailurecount = 0, 0
    rentalsuccesscount, rentalfailurecount = 0, 0

    # Process product file and add to mongoDB
    try:
        with open(Path(directory_name, product_file), 'r') as prodfile:

            next(prodfile) # skip header line

            with mongo:
                db = mongo.connection.HPNorton
                productcollection = db["products"]

                for line in prodfile:
                    linelist = [x.strip() for x in line.split(',')]

                    try:
                        result = productcollection.insert_one(
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

                    except errors.DuplicateKeyError:
                        productfailurecount += 1
                        continue

                    DBLOG.info(f'Added product DB entry: {linelist[0]}')

    except FileNotFoundError as fileerror:
        SYSTEMLOG.error(f'File not found at {directory_name + product_file}, exception {type(fileerror).__name__}')

    # Process customer file and add to mongoDB
    try:
        with open(Path(directory_name, customer_file), 'r') as custfile:

            next(custfile) # skip header line
            with mongo:
                db = mongo.connection.HPNorton
                customercollection = db["customers"]
                for line in custfile:
                    linelist = [x.strip() for x in line.split(',')]

                    result = customercollection.insert_one(
                        {
                            'customer_id' : linelist[0],
                            'name' : linelist[1],
                            'address' : linelist[2],
                            'zip_code' : linelist[3],
                            'phone_number' : linelist[4],
                            'email' : linelist[5],
                            'rentals' : []
                        })

                    if result.acknowledged:
                        customersuccesscount += 1
                    else:
                        customerfailurecount += 1

                    DBLOG.info(f'Added customer DB entry: {linelist[0]}')

    except FileNotFoundError as fileerror:
        SYSTEMLOG.error(f'File not found at {directory_name + product_file}, exception {type(fileerror).__name__}')

    # Process rental file and add to mongoDB in customer collection
    try:
        with open(Path(directory_name, rentals_file), 'r') as rentfile:

            next(rentfile) # skip header line

            with mongo:
                db = mongo.connection.HPNorton
                customercollection = db["customers"]
                for line in rentfile:
                    linelist = [x.strip() for x in line.split(',')]

                    result = customercollection.update_one(
                        {
                            'customer_id' : linelist[1]
                        },
                        {
                            '$addToSet' :
                            {
                                'rentals' : linelist[0]
                            }
                        })

                    if result.modified_count:
                        rentalsuccesscount += 1
                    else:
                        rentalfailurecount += 1

                    DBLOG.info(f'Added rental DB entry to customer: {linelist[1]}')

    except FileNotFoundError as fileerror:
        SYSTEMLOG.error(f'File not found at {directory_name + product_file}, exception {type(fileerror).__name__}')

    return (productsuccesscount, customersuccesscount, rentalsuccesscount), (productfailurecount, customerfailurecount, rentalfailurecount)


def show_available_products():
    """ Returns all products with quantity greater than 0 """

    mongo = MongoDBConnection()
    result = {}

    with mongo:
        db = mongo.connection.HPNorton
        productcollection = db["products"]
        for document in productcollection.find({"quantity_available": {"$gt": "0"}}):
            key = document['product_id']

            result[key] = {
                'description': document['description'],
                'product_type': document['product_type'],
                'quantity_available': document['quantity_available']
                }

    return result


def show_rentals(product_id):
    """
    Returns dictionary of customers with the provided
    product_id in the rentals field.

    :param: product id rented by a customer
    """

    mongo = MongoDBConnection()

    result = {}
    with mongo:
        db = mongo.connection.HPNorton
        customercollection = db["customers"]
        for document in customercollection.find({"rentals": {"$in": [product_id]}}):
            key = document['customer_id']

            result[key] = {
                'name': document['name'],
                'address': document['address'],
                'phone_number': document['phone_number'],
                'email': document['email']
                }

    return result
