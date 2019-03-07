""" Lesson 08 HPNorton furniture rental """


from pathlib import Path
import os
import logging

LOG_FORMAT = "%(asctime)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE_SYSTEM = 'system.log'

FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER_SYSTEM = logging.FileHandler(LOG_FILE_SYSTEM, mode='w')
FILE_HANDLER_SYSTEM.setFormatter(FORMATTER)

# General logging
SYSTEMLOG = logging.getLogger('SYSTEMLOG')
SYSTEMLOG.addHandler(FILE_HANDLER_SYSTEM)
SYSTEMLOG.setLevel("INFO")

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """ Creates or appends to invoice file using arguments provided """

    directory_name = os.path.dirname(os.path.abspath(__file__))

    try:
        with open(Path(directory_name, invoice_file), 'a') as furniture_invoice:
            furniture_invoice.write(f'{customer_name}, {item_code}, {item_description}, {item_monthly_price}\n')

            SYSTEMLOG.info(f'Data added to invoice file: {customer_name}, {item_code}, {item_description}, {item_monthly_price}')

    except IOError as fileerror:
        SYSTEMLOG.error(f'File error {directory_name + invoice_file}, exception {type(fileerror).__name__}')


def single_customer(customer_name, invoice_file):
    """ Provides a function """

    def consumerentalitems(rental_items):
        """ Add rental times to invoice file """

        directory_name = os.path.dirname(os.path.abspath(__file__))
        try:
            with open(Path(directory_name,invoice_file), 'a') as output_file:
                with open(Path(directory_name,rental_items), 'r') as input_file:

                    for line in input_file:
                        fields = line.strip().split(',')
                        output_file.write(f'{customer_name}, {fields[0]}, {fields[1]}, {fields[2]}\n')
                        SYSTEMLOG.info(f'Data added to invoice file {invoice_file}: {customer_name}, {fields[0]}, {fields[1]}, {fields[2]}')

        except IOError as fileerror:
            SYSTEMLOG.error(f'File error {directory_name + invoice_file}, exception {type(fileerror).__name__}')

    return consumerentalitems

if __name__ == "__main__":

    add_furniture('testfile', 'Elisa Miles','LR04','Leather Sofa', 25.00)
