import threading
import time

from loguru import logger
from sys import stdout

from ingest_csv import ingest_customer_csv
from ingest_csv import ingest_product_csv
from ingest_csv import ingest_rental_csv

from database import Connection
from database import show_available_products
from database import show_rentals

from models import util_drop_all

CUST_CSV_FILENAME = 'customers.csv'
PROD_CSV_FILENAME = 'products.csv'
RNTL_CSV_FILENAME = 'rentals.csv'
#CSV_PATH_DBG = './lessons/lesson05/assignment/'
CSV_PATH_DBG = ''


def parallel():
    """
    Ensure you application will create an empty database if one doesn’t exist
    when the app is first run. Call it customers.db
    """

    # Standalone function to initialize logging
    logger.add(stdout, level='WARNING')
    logger.add("logfile_{time}.txt", level='INFO')
    logger.enable(__name__)

    with Connection():
        util_drop_all()

    cust_thread = threading.Thread(target=ingest_customer_csv,
                                   args=(CSV_PATH_DBG + CUST_CSV_FILENAME, True))
    prod_thread = threading.Thread(target=ingest_product_csv, 
                                   args=(CSV_PATH_DBG + PROD_CSV_FILENAME, True))
    rent_thread = threading.Thread(target=ingest_rental_csv,
                                   args=(CSV_PATH_DBG + RNTL_CSV_FILENAME, True))

    start = time.perf_counter()

    cust_thread.start()
    prod_thread.start()
    rent_thread.start()

    # wait until all threads are done
    cust_thread.join()
    prod_thread.join()
    rent_thread.join()

    elapsed = time.perf_counter() - start
    print(f"{__file__} db ingest executed in {elapsed:0.2f}")

    db_dict = show_available_products()

    print(db_dict)

    db_dict = show_rentals('prd002')

    print(db_dict)
