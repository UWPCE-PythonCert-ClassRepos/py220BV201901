"""
ingest_csv.py module uses generator to perform per-line import
from specified CSV file and ingest as record into sqlite3 db
using basic_operations.py
"""

from loguru import logger

from models import Customer
from models import Product
from models import Rental



# indexes into array returned by CSV reader
CUST_USERID = 0
CUST_NAME = 1
CUST_ADDRESS = 2
CUST_ZIPCODE = 3
CUST_PHONE = 4
CUST_EMAIL = 5

PROD_ID = 0
PROD_DESC = 1
PROD_TYPE = 2
PROD_QTY = 3

RENTAL_PROD_ID = 0
RENTAL_USER_ID = 1


def import_csv_gen(csv_filename):
    """
    Import csv file generator (yields one record per yield)
    """
    with open(csv_filename, 'r') as csv_fd:
        line_num = 0
        line = 'foo'
        while line:
            line_num += 1
            try:
                line = csv_fd.readline()
                # generator 'yield' statement for each
                # line of the CSV file below. Python CSV
                # support does not allow per-line parsing
                yield line.rstrip('\n').split(',')
            except EOFError:
                return


def ingest_customer_csv(csv_path):
    """
    Ingest csv function to combine extract and import gen functions,
    and populate data from generator in database
    """
    # Create a CSV import generator (next yields one db row)
    import_generator = import_csv_gen(csv_path)
    # Skip over the title row
    next(import_generator)
    # Iterate over all other rows
    while True:
        try:
            data = next(import_generator)
            if len(data) != 8:
                logger.error(f'Data with incorrect item count: {len(data)}')
                continue
            # extract items from list and add record to database
            customer = Customer(
                user_id = data[CUST_USERID],
                name = data[CUST_NAME],
                address = data[CUST_ADDRESS],
                zip_code = int(data[CUST_ZIPCODE]),
                phone_number = data[CUST_PHONE],
                email = data[CUST_EMAIL]
            )
            customer.save()
        except StopIteration:
            break


def ingest_product_csv(csv_path):
    """
    Ingest csv function to combine extract and import gen functions,
    and populate data from generator in database
    """
    # Create a CSV import generator (next yields one db row)
    import_generator = import_csv_gen(csv_path)
    # Skip over the title row
    next(import_generator)
    # Iterate over all other rows
    while True:
        try:
            data = next(import_generator)
            if len(data) != 4:
                logger.error(f'Data with incorrect item count: {len(data)}')
                continue
            product = Product(
                product_id=data[PROD_ID],
                description=data[PROD_DESC],
                product_type=data[PROD_TYPE],
                quantity_available=data[PROD_QTY]
            )
            product.save()
        except StopIteration:
            break


def ingest_rental_csv(csv_path):
    """
    Ingest csv function to combine extract and import gen functions,
    and populate data from generator in database
    """
    # Create a CSV import generator (next yields one db row)
    import_generator = import_csv_gen(csv_path)
    # Skip over the title row
    next(import_generator)
    # Iterate over all other rows
    while True:
        try:
            data = next(import_generator)
            if len(data) != 2:
                logger.error(f'Data with incorrect item count: {len(data)}')
                continue
            # extract items from list and add record to database
            rental = Rental(
                prod_id=data[RENTAL_PROD_ID],
                user_id=data[RENTAL_USER_ID]
            )
            rental.save()       # This will perform an insert
        except StopIteration:
            break
