"""
ingest_csv.py module uses generator to perform per-line import
from specified CSV file and ingest as document into mongodb
"""

import threading

from zipfile import ZipFile

from loguru import logger

from models import Customer
from models import Product
from models import Rental

from database import Connection

DATA_ZIP_FILENAME = './lessons/lesson07/assignment/data.zip'
#DATA_ZIP_FILENAME = './data.zip'
CUST_CSV_FILENAME = 'customers.csv'
PROD_CSV_FILENAME = 'products.csv'
RENTAL_CSV_FILENAME = 'rentals.csv'
EXTRACT_PATH = './lessons/lesson07/assignment/'
# EXTRACT_PATH = './'

# indexes into array returned by CSV reader
CUST_USERID = 0
CUST_NAME = 1
CUST_LAST_NAME = 2
CUST_ADDRESS = 3
CUST_PHONE = 4
CUST_EMAIL = 5
CUST_STATUS = 6
CUST_CREDIT_LIMIT = 7

PROD_ID = 0
PROD_DESC = 1
PROD_TYPE = 2
PROD_QTY = 3

RENTAL_PROD_ID = 5
RENTAL_USER_ID = 0

extract_lock = threading.Lock()

def extract_csv(zip_filename, csv_filename, extract_path, with_lock):
    """
    Extract .csv file from .zip file (req'd for github file size limits)
    Use the _with_lock_ argument to specify whether a lock is held during
    the extraction for multithreaded operation
    """
    if with_lock is True:
        logger.info(f"Acquiring lock for {csv_filename}")
        extract_lock.acquire()
        logger.info(f"==> Lock acquired for {csv_filename}")
        with ZipFile(zip_filename, 'r') as ziparchive:
            # extract csv file using EXTRACT_PATH
            ziparchive.extract(csv_filename, path=extract_path)
        logger.info(f"Releasing lock for {csv_filename}")
        extract_lock.release()
    else:
        with ZipFile(zip_filename, 'r') as ziparchive:
            # extract csv file using EXTRACT_PATH
            ziparchive.extract(csv_filename, path=extract_path)


def import_csv_gen(csv_filename):
    """
    Import csv file generator (yields one record per yield)
    """
    with open(csv_filename, 'r') as csv_fd:
        line = 'foo'
        while line:
            try:
                line = csv_fd.readline()
                # generator 'yield' statement for each
                # line of the CSV file below. Python CSV
                # support does not allow per-line parsing
                yield line.rstrip('\n').split(',')
            except EOFError:
                return


def ingest_customer_csv_thread(*args, **kwargs):
    start = time.perf_counter()
    num_records = ingest_customer_csv(True)
    cust_elapsed = time.perf_counter() - start
    kwargs['num_records'] = num_records
    kwargs['elapsed_time'] = cust_elapsed


def ingest_customer_csv(with_lock):
    """
    Ingest csv function to combine extract and import gen functions,
    and populate data from generator in database
    """
    record_count = int(0)
    # Extract the CSV file from the zip archive
    extract_csv(DATA_ZIP_FILENAME, CUST_CSV_FILENAME, EXTRACT_PATH, with_lock)
    # Create a CSV import generator (next yields one db row)
    import_generator = import_csv_gen(EXTRACT_PATH + CUST_CSV_FILENAME)
    # Skip over the title row
    next(import_generator)
    # Iterate over all other rows
    with Connection():
        while True:
            try:
                data = next(import_generator)
                if len(data) != 8:
                    logger.error(f'Data item count: {len(data)}')
                    continue
                # extract items from list and add document to database
                customer = Customer(
                    user_id=data[CUST_USERID],
                    name=data[CUST_NAME],
                    last_name=data[CUST_LAST_NAME],
                    address=data[CUST_ADDRESS],
                    phone_number=data[CUST_PHONE],
                    email=data[CUST_EMAIL],
                    status=True if data[CUST_STATUS] == 'Active' else False,
                    credit_limit=int(data[CUST_CREDIT_LIMIT])
                )
                customer.save()       # This will perform an insert
                record_count += 1
            except StopIteration:
                break
    return record_count


def ingest_product_csv_thread(*args, **kwargs):
    start = time.perf_counter()
    num_records = ingest_product_csv(True)
    prod_elapsed = time.perf_counter() - start
    kwargs['num_records'] = num_records
    kwargs['elapsed_time'] = prod_elapsed


def ingest_product_csv(with_lock):
    """
    Ingest csv function to combine extract and import gen functions,
    and populate data from generator in database
    """
    record_count = int(0)
    # Extract the CSV file from the zip archive
    extract_csv(DATA_ZIP_FILENAME, PROD_CSV_FILENAME, EXTRACT_PATH, with_lock)
    # Create a CSV import generator (next yields one db row)
    import_generator = import_csv_gen(EXTRACT_PATH + PROD_CSV_FILENAME)
    # Skip over the title row
    next(import_generator)
    # Iterate over all other rows
    with Connection():
        while True:
            try:
                data = next(import_generator)
                if len(data) != 4:
                    logger.error(f'Data item count: {len(data)}')
                    continue
                # extract items from list and add document to database
                product = Product(
                    product_id=data[PROD_ID],
                    description=data[PROD_DESC],
                    product_type=data[PROD_TYPE],
                    quantity_available=data[PROD_QTY]
                )
                product.save()       # This will perform an insert
                record_count += 1
            except StopIteration:
                break
    return record_count

def ingest_rental_csv_thread(*args, **kwargs):
    start = time.perf_counter()
    num_records = ingest_rental_csv(True)
    rental_elapsed = time.perf_counter() - start
    kwargs['num_records'] = num_records
    kwargs['elapsed_time'] = rental_elapsed

def ingest_rental_csv(with_lock):
    """
    Ingest csv function to combine extract and import gen functions,
    and populate data from generator in database
    """
    record_count = int(0)
    # Extract the CSV file from the zip archive
    extract_csv(DATA_ZIP_FILENAME, RENTAL_CSV_FILENAME, EXTRACT_PATH, with_lock)
    # Create a CSV import generator (next yields one db row)
    import_generator = import_csv_gen(EXTRACT_PATH + RENTAL_CSV_FILENAME)
    # Skip over the title row
    next(import_generator)
    # Iterate over all other rows
    with Connection():
        while True:
            try:
                data = next(import_generator)
                if len(data) != 6:
                    logger.error(f'Data item count: {len(data)}')
                    continue
                # extract items from list and add document to database
                rental = Rental(
                    product_id=data[RENTAL_PROD_ID],
                    user_id=data[RENTAL_USER_ID]
                )
                rental.save()       # This will perform an insert
                record_count += 1
            except StopIteration:
                break
    return record_count
