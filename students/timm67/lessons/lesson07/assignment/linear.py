import time
from loguru import logger

from ingest_csv import ingest_customer_csv
from ingest_csv import ingest_product_csv
from ingest_csv import ingest_rental_csv

from database import Connection
from database import show_available_products
from database import show_rentals

from models import util_drop_all

def linear():
    """
    Each module will return a list of tuples, one tuple for customer
    and one for products. Each tuple will contain 4 values:
    - the number of records processed (int),
    - the record count in the database prior to running (int),
    - the record count after running (int),
    - the time taken to run the module (float).
    """

    logger.info("Drop all documents")
    with Connection():
        util_drop_all()

    start = time.perf_counter()

    num_cust_records = ingest_customer_csv(False)
    cust_elapsed = time.perf_counter() - start
    num_prod_records = ingest_product_csv(False)
    prod_elapsed = time.perf_counter() - cust_elapsed
    num_rental_records = ingest_rental_csv(False)
    rental_elapsed = time.perf_counter() - prod_elapsed

    ret_list = [
        (num_cust_records, 0, num_cust_records, cust_elapsed),
        (num_prod_records, 0, num_prod_records, prod_elapsed),
        (num_rental_records, 0, num_rental_records, rental_elapsed)
    ]

    return ret_list
