from sys import stdout
from csv import reader as csv_reader
from zipfile import ZipFile
from loguru import logger
from basic_operations import add_customer

ZIP_FILENAME = 'customer.zip'
CSV_FILENAME = 'customer.csv'

# indexes into array returned by CSV reader
CUST_ID = 0
CUST_NAME = 1
CUST_LASTNAME = 2
CUST_ADDRESS = 3
CUST_PHONE = 4
CUST_EMAIL = 5
CUST_STATUS = 6
CUST_CREDIT_LIMIT = 7


def extract_csv(zip_filename):
    """
    Extract .csv file from .zip file (req'd for github file siz limits)
    """
    with ZipFile(zip_filename, 'r') as ziparchive:
        # extract all files in the zip archive
        ziparchive.extractall()


def import_csv_gen(csv_filename):
    """
    Import csv file generator (yields one record per next())
    """
    with open(csv_filename, 'r') as csv_fd:
        myreader = csv_reader(csv_fd.readline())
        line = myreader()
        while line != []:
            yield line
            line = myreader()


def ingest_csv():
    """
    Ingest csv function to combine extract and import gen functions,
    and populate data from generator in database
    """
    kwargs = {}
    # Extract the CSV file from the zip archive
    extract_csv(ZIP_FILENAME)
    # Create a CSV import generator (next yields one db row)
    import_generator = import_csv_gen(CSV_FILENAME)
    # Skip over the title row
    next(import_generator)
    # Iterate over all other rows
    while True:
        try:
            data = next(import_generator)
            # extract items from list and add record to database
            kwargs['customer_id'] = data[CUST_ID]
            kwargs['name'] = data[CUST_NAME]
            kwargs['lastname'] = data[CUST_LASTNAME]
            kwargs['home_address'] = data[CUST_ADDRESS]
            kwargs['phone_number'] = data[CUST_PHONE]
            kwargs['email_address'] = data[CUST_EMAIL]
            kwargs['status'] = data[CUST_STATUS]
            kwargs['credit_limit'] = data[CUST_CREDIT_LIMIT]
            try:
                add_customer(**kwargs)
            except ValueError:
                logger.error(f'Unable to add {data[CUST_ID]} to database')
        except StopIteration:
            break
