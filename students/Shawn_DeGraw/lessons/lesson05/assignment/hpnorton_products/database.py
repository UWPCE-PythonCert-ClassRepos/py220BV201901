"""
HP Norton operations for MongoDB
"""

import logging
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

MYCLIENT = pymongo.MongoClient("mongodb://localhost:27017/")
MYDB = MYCLIENT["HPNorton"]

PRODUCTCOLLECTION = MYDB["products"]
CUSTOMERCOLLECTION = MYDB["customers"]


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


    try:
        with open(Path(directory_name) + product_file, 'r') as prodfile:

            for line in prodfile:
                linelist = line.split(',')

                result = MYDB.PRODUCTCOLLECTION.insert(
                            {
                                linelist[0] :
                                    {
                                        'description' : linelist[1],
                                        'product_type' : linelist[2],
                                        'quantity_available' : linelist[3]
                                    }
                            })

                if result.WriteResult["nInserted"]:
                    productsuccesscount += 1
                else:
                    productfailurecount += 1

                DBLOG.info(f'Added product DB entry: {linelist[0]}')

    except FileNotFoundError as fileerror:
        SYSTEMLOG.error(f'File not found at {directory_name + product_file}, exception {type(fileerror).__name__}')


    try:
        with open(Path(directory_name) + customer_file, 'r') as custfile:

            for line in custfile:
                linelist = line.split(',')

                result = MYDB.CUSTOMERCOLLECTION.insert(
                            {
                                linelist[0] :
                                    {
                                        'name' : linelist[1],
                                        'address' : linelist[2],
                                        'zip_code' : linelist[3],
                                        'phone_number' : linelist[4],
                                        'email' : linelist[5],
                                        'rentals' : []
                                    }
                            })

                if result.WriteResult["nInserted"]:
                    customersuccesscount += 1
                else:
                    customerfailurecount += 1

                DBLOG.info(f'Added customer DB entry: {linelist[0]}')

    except FileNotFoundError as fileerror:
        SYSTEMLOG.error(f'File not found at {directory_name + product_file}, exception {type(fileerror).__name__}')


    try:
        with open(Path(directory_name) + rentals_file, 'r') as rentfile:

            for line in rentfile:
                linelist = line.split(',')

                result = MYDB.CUSTOMERCOLLECTION.updateOne(
                            { linelist[1] },
                            { $addToSet: { 'rentals' : [ linelist[0] ] } } )

                if result.WriteResult["modifiedCount"]:
                    rentalsuccesscount += 1
                else:
                    rentalfailurecount += 1

                DBLOG.info(f'Added rental DB entry to customer: {linelist[1]}')

    except FileNotFoundError as fileerror:
        SYSTEMLOG.error(f'File not found at {directory_name + product_file}, exception {type(fileerror).__name__}')
