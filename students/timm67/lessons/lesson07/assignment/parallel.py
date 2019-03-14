import threading

from loguru import logger

from ingest_csv import ingest_customer_csv_thread
from ingest_csv import ingest_product_csv_thread
from ingest_csv import ingest_rental_csv_thread
from ingest_csv import get_retval_thread

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
    ret_list = []

    logger.info("Drop all documents")
    with Connection():
        util_drop_all()

    # Create the threads; one for each mongo document
    cust_thread = threading.Thread(target=ingest_customer_csv_thread)
    prod_thread = threading.Thread(target=ingest_product_csv_thread)
    rental_thread = threading.Thread(target=ingest_rental_csv_thread)

    # Start the threads
    cust_thread.start()
    prod_thread.start()
    rental_thread.start()

    #
    # Wait (block) until all threads are done. It is possible that the
    # waiting order might affect the performance if the shortest running
    # thread is not joined first. I based the order on the runtime
    # returned from the threading 
    #
    cust_thread.join()
    rental_thread.join()
    prod_thread.join()

    #
    # Get the results of each thread. The thread name will be added to the
    # tuple, because we don't know what order the threads finish up in
    # each time
    #
    ret_list.append(get_retval_thread())
    ret_list.append(get_retval_thread())
    ret_list.append(get_retval_thread())

    return ret_list
