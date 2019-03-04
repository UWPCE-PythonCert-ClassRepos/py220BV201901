"""
Placeholder for unit tests. May be able to use mongomock if ready

from mongoengine import connect
db = connect('test')
db.drop_database('test')

"""

import sys
from mongoengine import connect
from loguru import logger

from models import util_drop_all

from database import Connection
from database import show_available_products
from database import show_rentals

from ingest_csv import ingest_customer_csv
from ingest_csv import ingest_product_csv
from ingest_csv import ingest_rental_csv

CUST_CSV_FILENAME = 'customers.csv'
PROD_CSV_FILENAME = 'products.csv'
RNTL_CSV_FILENAME = 'rentals.csv'
#CSV_PATH_DBG = './lessons/lesson05/assignment/'
CSV_PATH_DBG = ''


# Standalone function to initialize logging
logger.add(stdout, level='WARNING')
logger.add("test_logfile_{time}.txt", level='INFO')
logger.enable(__name__)


def test_00setup():
    # connect and drop the current database
    with Connection():
        util_drop_all()

    # create the test database
    ingest_customer_csv(CSV_PATH_DBG + CUST_CSV_FILENAME)
    ingest_product_csv(CSV_PATH_DBG + PROD_CSV_FILENAME)
    ingest_rental_csv(CSV_PATH_DBG + RNTL_CSV_FILENAME)

def test_10show_avail_products():
    db_dict = show_available_products()

def test_99teardown():
    # connect and drop the test database
    with Connection():
        util_drop_all()
