"""
    Autograde Lesson 8 assignment

"""

import pytest

from lessons.lesson08.assignment import inventory as l



def test_add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    l.add_furniture("invoice01.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    l.add_furniture("invoice01.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    l.add_furniture("invoice01.csv", "Alex Gonzales", "Queen Mattress", 17)


def single_customer(customer_name, invoice_file):
    create_invoice = l.single_customer("Susan Wong", "SW_invoice.csv")
    create_invoice("test_items.csv")