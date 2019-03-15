"""
Unit test for inventory module

Assumes SW_invoice.csv file already exists in the form of:
item_code, item_description, item_monthly_price
"""

import os
from inventory import *

# create variables for testing
FILE_NM = "invoice01.csv"

FURNITURE_TEST = [["Elisa Miles", "LR04", "Leather Sofa", '25'],
                  ["Edward Data", "KT78", "Kitchen Table", '10'],
                  ["Alex Gonzales", "BR02", "Queen Mattress", '17']]

CUSTOMER_TEST = [["Susan Wong", "LR04", "Leather Sofa", '25'],
                 ["Susan Wong", "KT78", "Kitchen Table", '10'],
                 ["Susan Wong", "BR02", "Queen Mattress", '17']]


def test_add_furniture():
    """ test for add_furniture function """
    test_list = []
    for row in FURNITURE_TEST:
        add_furniture(FILE_NM, row[0], row[1], row[2], row[3])

    # read test file to list of lists
    with open(FILE_NM, mode="r", newline="") as csv_file:
        reader = csv.reader(csv_file)
        test_list = list(list(row) for row in csv.reader(csv_file, delimiter=','))

    assert FURNITURE_TEST[0] == test_list[0]
    assert FURNITURE_TEST[1] == test_list[1]
    assert FURNITURE_TEST[2] == test_list[2]

    os.remove(FILE_NM)


def test_single_customer():
    """ test for single_customer function """
    test_list = []
    create_invoice = single_customer("Susan Wong", "SW_invoice.csv")
    create_invoice(FILE_NM)

    # read test file to list of lists
    with open(FILE_NM, mode="r", newline="") as csv_file:
        reader = csv.reader(csv_file)
        test_list = list(list(row) for row in csv.reader(csv_file, delimiter=','))

    assert CUSTOMER_TEST[0] == test_list[0]
    assert CUSTOMER_TEST[1] == test_list[1]
    assert CUSTOMER_TEST[2] == test_list[2]

    os.remove(FILE_NM)
