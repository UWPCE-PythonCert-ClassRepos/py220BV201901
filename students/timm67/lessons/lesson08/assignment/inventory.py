""" Functional Techniques assignment"""

import csv
from functools import partial
from itertools import chain

"""
Input paramters: inventory_file, customer_name, item_code
    item_description, item_monthly_price

This function will create inventory_file if it doesn't exist
or append a new line to it if it does. After adding a few
items to the same file, the file created by add_furniture
should look something like this:

Elisa Miles,LR04,Leather Sofa,25.00
Edward Data,KT78,Kitchen Table,10.00
Alex Gonzales,BR02,Queen Mattress,17.00
"""

def add_furniture(inventory_file, customer_name, item_code,
                  item_description, item_monthly_price):
    """ add inventory items to inventory_file """
    with open(inventory_file, 'a+') as csv_fp:
        csv_writer = csv.writer(csv_fp)
        row = [customer_name, item_code, item_description,
               item_monthly_price]
        csv_writer.writerow(row)


"""
Input parameters: invoice_file, customer_name
Output: Returns a function that takes one parameter, rental_items.

single_customer needs to use functools.partial and closures, 
in order to return a function that will iterate through rental_items 
and add each item to invoice_file.
"""
def single_customer(customer_name, invoice_file):
    """return a fn that adds rental_items to invoice_file """
    def single_customer_items(items_file):
        """ read from items_file, and create invoice using cust name"""
        add_items = []
        with open(items_file, 'r') as items_fp:
            items_reader = csv.reader(items_fp)
            for item in items_reader:
                add_items.append(list(chain([customer_name], item)))

        with open(invoice_file, 'a+') as invoice_fp:
            invoice_writer = csv.writer(invoice_fp)
            for item in add_items:
                invoice_writer.writerow(item)

    return single_customer_items
