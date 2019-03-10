import threading
import time

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
    Ensure you application will create an empty database if one doesn’t exist
    when the app is first run. Call it customers.db
    """

    logger.info("Drop all documents")
    with Connection():
        util_drop_all()

    cust_thread = threading.Thread(target=ingest_customer_csv_thread)
    prod_thread = threading.Thread(target=ingest_product_csv_thread)
    rent_thread = threading.Thread(target=ingest_rental_csv_thread)

    start = time.perf_counter()

    cust_thread.start()
    prod_thread.start()
    rent_thread.start()

    # wait until all threads are done
    cust_thread.join()
    prod_thread.join()
    rent_thread.join()

    elapsed = time.perf_counter() - start
    print(f"parallel db ingest executed in {elapsed:0.4f} seconds")
    logger.info(f"parallel db ingest executed in {elapsed:0.4f} seconds")

    # db_dict = show_available_products()

    # print(db_dict)

    # db_dict = show_rentals('P000002')

    # print(db_dict)
