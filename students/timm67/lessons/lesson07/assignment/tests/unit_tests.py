"""

Setup/teardown example:
Everything after yield is teardown / evthing before is setup

import smtplib
import pytest

@pytest.fixture(scope="module")
def smtp_connection():
    smtp_connection = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
    yield smtp_connection  # provide the fixture value
    print("teardown smtp")
    smtp_connection.close()
"""

import sys
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
#CSV_PATH_DBG = './lessons/lesson07/assignment/'
CSV_PATH_DBG = ''


# Standalone function to initialize logging
logger.add(sys.stdout, level='WARNING')
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
    db_dict_actual = {
    'prd001': {'description': '60-inch TV stand', 'product_type': 'livingroom', 'quantity_available': 3},
    'prd002': {'description': 'L-shaped sofa', 'product_type': 'livingroom', 'quantity_available': 0},
    'prd003': {'description': 'Acacia kitchen table', 'product_type': 'kitchen', 'quantity_available': 7},
    'prd004': {'description': 'Queen bed', 'product_type': 'bedroom', 'quantity_available': 10},
    'prd005': {'description': 'Reading lamp', 'product_type': 'bedroom', 'quantity_available': 20},
    'prd006': {'description': 'Portable heater', 'product_type': 'bathroom', 'quantity_available': 14},
    'prd007': {'description': 'Ballerina painting', 'product_type': 'livingroom', 'quantity_available': 0},
    'prd008': {'description': 'Smart microwave', 'product_type': 'kitchen', 'quantity_available': 30},
    'prd009': {'description': 'Popcorn machine', 'product_type': 'kitchen', 'quantity_available': 0},
    'prd010': {'description': '60-inch TV', 'product_type': 'livingroom', 'quantity_available': 3}}

    db_dict = show_available_products()

    for item in db_dict_actual.keys():
        assert db_dict[item] == db_dict_actual[item]

def test_20show_rentals():
    db_dict_actual = {
    'user008': {'name': 'Shirlene Harris', 'address': '4329 Honeysuckle Lane', 'phone_number': '206-279-5340', 'email': 'harrisfamily@gmail.com'},
    'user005': {'name': 'Dan Sounders', 'address': '861 Honeysuckle Lane', 'phone_number': '206-279-1723', 'email': 'soundersoccer@mls.com'}}

    db_dict = show_rentals('prd002')

    for item in db_dict_actual.keys():
        assert db_dict[item] == db_dict_actual[item]

def test_99teardown():
    # connect and drop the test database
    with Connection():
        util_drop_all()
