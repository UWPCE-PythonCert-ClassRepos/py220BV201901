import threading

from loguru import logger

from ingest_csv import ingest_customer_csv_thread
from ingest_csv import ingest_product_csv_thread
from ingest_csv import ingest_rental_csv_thread

from database import Connection
from database import show_available_products
from database import show_rentals

from models import util_drop_all


def parallel():
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

    cust_kwargs = {}
    prod_kwargs = {}
    rental_kwargs = {}

    cust_thread = threading.Thread(target=ingest_customer_csv_thread,
                                   kwargs=cust_kwargs)
    prod_thread = threading.Thread(target=ingest_product_csv_thread,
                                   kwargs=prod_kwargs)
    rental_thread = threading.Thread(target=ingest_rental_csv_thread,
                                     kwargs=rental_kwargs)

    cust_thread.start()
    prod_thread.start()
    rental_thread.start()

    # wait until all threads are done
    cust_thread.join()
    prod_thread.join()
    rental_thread.join()

    ret_list = [
        (cust_kwargs['num_records'], 0, cust_kwargs['num_records'],
         cust_kwargs['elapsed_time']),
        (prod_kwargs['num_records'], 0, prod_kwargs['num_records'],
         prod_kwargs['elapsed_time']),
        (rental_kwargs['num_records'], 0, rental_kwargs['num_records'],
         rental_kwargs['elapsed_time'])
    ]

    return ret_list
