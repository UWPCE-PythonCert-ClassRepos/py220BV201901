from sys import stdout
import io
import csv
from zipfile import ZipFile
from loguru import logger
from basic_operations import add_customer

ZIP_FILENAME = './lessons/lesson04/assignment/customer.zip'
CSV_FILENAME = 'customer.csv'
EXTRACT_PATH = './lessons/lesson04/assignment/'

# indexes into array returned by CSV reader
CUST_ID = 0
CUST_NAME = 1
CUST_LASTNAME = 2
CUST_ADDRESS = 3
CUST_PHONE = 4
CUST_EMAIL = 5
CUST_STATUS = 6
CUST_CREDIT_LIMIT = 7


def extract_csv(zip_filename, csv_filename, extract_path):
    """
    Extract .csv file from .zip file (req'd for github file size limits)
    """
    with ZipFile(zip_filename, 'r') as ziparchive:
        # extract csv file using EXTRACT_PATH
        ziparchive.extract(csv_filename, path=extract_path)


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
                yield line.rstrip('\n').split(',')
            except EOFError:
                return



def ingest_csv():
    """
    Ingest csv function to combine extract and import gen functions,
    and populate data from generator in database
    """

    # Extract the CSV file from the zip archive
    extract_csv(ZIP_FILENAME, CSV_FILENAME, EXTRACT_PATH)
    # Create a CSV import generator (next yields one db row)
    import_generator = import_csv_gen(EXTRACT_PATH + CSV_FILENAME)
    # Skip over the title row
    next(import_generator)
    # Iterate over all other rows
    while True:
        kwargs = {}
        try:
            data = next(import_generator)
            if len(data) != 8:
                logger.error(f'Got data item with incorrect item count: {len(data)}')
                continue
            # extract items from list and add record to database
            kwargs['customer_id'] = data[CUST_ID]
            kwargs['name'] = data[CUST_NAME]
            kwargs['lastname'] = data[CUST_LASTNAME]
            kwargs['home_address'] = data[CUST_ADDRESS]
            kwargs['phone_number'] = data[CUST_PHONE]
            kwargs['email_address'] = data[CUST_EMAIL]
            kwargs['status'] = data[CUST_STATUS]
            kwargs['credit_limit'] = float(data[CUST_CREDIT_LIMIT])
            try:
                add_customer(**kwargs)
            except ValueError:
                logger.error(f'Unable to add {data[CUST_ID]} to database')
        except StopIteration:
            break
