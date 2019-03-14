""""
Module to create and modify inventory invoice's that contain customer
and rental information
"""

import csv

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """ adds customer name and rental details to a csv file """
    with open(invoice_file, mode="a", newline="") as csv_file:
        csv.writer(csv_file).writerow([customer_name,
                                       item_code,
                                       item_description,
                                       item_monthly_price])


def single_customer(customer_name, invoice_file):
    """ curried function to create an invoice for a single customer """
    invoice_data = []

    def create_invoice(inventory_file):

    # open csv invoice file and read data
        with open(invoice_file, mode="r", newline="") as csv_file:
            for row in csv_file:
                invoice_row = list(row.strip().split(','))
                invoice_data.append(invoice_row)

        # open csv inventory file and write data
        with open(inventory_file, mode="a", newline="") as csv_file:
            for row in invoice_data:
                csv.writer(csv_file).writerow([customer_name,
                                               row[0],
                                               row[1],
                                               row[2]])
    return create_invoice
