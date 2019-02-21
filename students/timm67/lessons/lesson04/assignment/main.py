from basic_operations import add_customer
from basic_operations import search_customer
from basic_operations import delete_customer
from basic_operations import update_customer_credit
from basic_operations import list_active_customers

from loguru import logger
from sys import stdout

from ingest_csv import ingest_csv

def main():
    """
    Ensure you application will create an empty database if one doesn’t exist
    when the app is first run. Call it customers.db
    """

    # Standalone function to initialize logging

    logger.add(stdout, level='INFO')
    logger.add("logfile_{time}.txt", level='DEBUG')
    logger.enable(__name__)

    # TODO: load the CSV file using generator and doing profiling
    ingest_csv_gen = ingest_csv()

    #
    # ingest_csv contains the generator function that iterates through the CSV
    # file parsing the CSV into a list of items
    #
    while True:
        try:
            db_row = next(ingest_csv_gen)
            # TODO: add db_row to the database
        catch StopIteration:
            break


if  __name__ == '__main__':
    main()
