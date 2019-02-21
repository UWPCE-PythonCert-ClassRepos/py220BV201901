from basic_operations import add_customer
from basic_operations import search_customer
from basic_operations import delete_customer
from basic_operations import update_customer_credit
from basic_operations import list_active_customers

from loguru import logger
from sys import stdout
from csv import reader as csv_reader

from zipfile import ZipFile

# indeces into array returned by CSV reader
cust_id = 0
cust_name = 1
zip_filename = 'customer.zip'
csv_filename = 'customer.csv'

def extract_csv(zip_filename):
    # opening the zip file in READ mode 
    with ZipFile(zip_filename, 'r') as zip:
        # extracting all the files 
        print('Extracting all the files now...') 
        zip.extractall() 


def import_csv(csv_filename):
    with open(csv_filename, 'r') as csv_fd:
        myreader = csv_reader(csv_fd.readline())
        line = myreader()
        while line != []:
            line = myreader()
            yield line
