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

from linear import linear

CUST_CSV_FILENAME = 'customers.csv'
PROD_CSV_FILENAME = 'products.csv'
RNTL_CSV_FILENAME = 'rentals.csv'
#CSV_PATH_DBG = './lessons/lesson07/assignment/'
CSV_PATH_DBG = ''

# Standalone function to initialize logging
logger.add(sys.stdout, level='WARNING')
logger.add("test_logfile_{time}.txt", level='INFO')
logger.enable(__name__)

ret_result = []

def test_00setup():
    global ret_result

    # connect and drop the current database
    with Connection():
        util_drop_all()

    # create the test database
    ret_result = linear()

def test_02check_ingest():
    global ret_result

    assert ret_result[0][0] == 'customer'
    assert ret_result[0][3] == 9999
    assert ret_result[0][4] > 2.0

    assert ret_result[1][0] == 'product'
    assert ret_result[1][3] == 9999
    assert ret_result[1][4] > 2.0

    assert ret_result[2][0] == 'rental'
    assert ret_result[2][3] == 9999
    assert ret_result[2][4] > 2.0


def test_20show_rentals():
    db_actual_dict = {
        'C000001': {'name': 'Shea', 'address': '3343 Sallie Gateway', 'phone_number': '508.104.0644 x4976', 'email': 'Alexander.Weber@monroe.com'},
        'C000003': {'name': 'Elfrieda', 'address': '3180 Mose Row', 'phone_number': '(839)825-0058', 'email': 'Mylene_Smitham@hannah.co.uk'}}

    db_ret_dict = show_rentals('P000003')

    for item in db_actual_dict:
        assert db_ret_dict[item] == db_actual_dict[item]
