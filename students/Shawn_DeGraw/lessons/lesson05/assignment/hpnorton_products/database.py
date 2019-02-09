"""
HP Norton operations for MongoDB
"""

import pymongo
import os
import logging
from pathlib import Path


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

MYCLIENT = pymongo.MongoClient("mongodb://localhost:27017/")
MYDB = MYCLIENT["HPNorton"]

productcollection = MYDB["products"]
customercollection = MYDB["customers"]


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Writes file data to Mongo DB.
    example: <import_data(directory_name, product_file, customer_file, rentals_file)>

    :param: directory_name - location of files using forward slashes
    :param: product_file - comma separated file of products
    :param: customer_file - comma separated file of customers
    :param: rentals_file - comma separated file of rentals by customer
    """

    try:
        with open(Path(directory_name) + product_file, 'r') as prodfile:

            for line in prodfile:
                linelist = line.split(',')

                MYDB.productcollection.insert(
                    {
                        linelist[0] :
                            {
                                'description' : linelist[1],
                                'product_type' : linelist[2],
                                'quantity_available' : linelist[3]
                            }
                    })

                DBLOG.info(f'Added product DB entry: {linelist[0]}')

    except FileNotFoundError as fileerror:
        SYSTEMLOG.error(f'File not found at {directory_name + product_file}, exception {type(fileerror).__name__}')
