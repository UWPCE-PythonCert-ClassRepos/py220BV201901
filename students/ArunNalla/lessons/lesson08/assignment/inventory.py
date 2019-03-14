#!usr/bin/env python3
"""Assingment Lesson08
By Arun Nalla 3/11/2019"""

import csv
from functools import partial
import logging

LOG_FORMAT = ("%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s")
logging.basicConfig(filename="inventory.log", level=logging.INFO,
                    format=LOG_FORMAT)

def add_furniture(invoice_file, customer_name, item_code,
                  item_description, item_monthly_price):
    """Function to create a new or add to an
    existing file = 'invoice_file'.
    Added arguments to file as provided"""
    try:
        with open(invoice_file, 'a', newline='') as file:
            logging.info(f' "{invoice_file}" has been opened.')
            invoice = csv.writer(file)
            invoice.writerow([customer_name, item_code, item_description,
                              float(item_monthly_price)])
            logging.info('Appended items to file.')
    except FileNotFoundError:
        logging.error(f'{file} not in folder')
    except Exception as err:
        logging.error(f'"{type(err)}" occured reading: "{file}"')

def single_customer(customer_name, invoice_file):
    """ Function using PARTIAL tool from functools
    to write adapt currying like"""
    try:
        first_func = partial(add_furniture, invoice_file, customer_name)
        logging.info('Bind two args from add_furniture to new function:'
                     'first_func')
    except Exception as err2:
        logging.error(f'"{type(err2)}" occured during functional binding')
    finally:
        def rentals_file(some_file):
            """Inner function to read rental file and
            append to a csv file"""
            try:
                with open(some_file, 'r') as file_2:
                    for row in csv.reader(file_2):
                        second_func = partial(first_func, *row)
                        logging.info('Bind rest of the args to second_func')
                        second_func()
            except Exception as err3:
                logging.error(f'"{type(err3)}" occured during currying')
    logging.info('Successfully curried and appended toimport  invoice file')
    return rentals_file

if __name__ == "__main__":
    # add_furniture('invoice01.csv', 'Elisa Miles', 'LR04',
    #               'Leather Sofa', 25.00)
    # add_furniture('invoice01.csv', 'Edward Data', 'KT78',
    #               'Kitchen Table', 10.00)
    # add_furniture('invoice01.csv', 'Alex Gonzales', 'BR02',
    #               'Queen Mattress', 17.00)

    CREATE_INVOICE = single_customer("Susan Wong", "SW_invoice.csv")
    CREATE_INVOICE("test_items.csv")
    # CREATE_INVOICE = single_customer("Susan Wong", "invoice01.csv")
    # CREATE_INVOICE("test_items.csv")
