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
    Ensure you application will create an empty database if one doesn’t exist
    when the app is first run. Call it customers.db
    """

    with Connection():
        util_drop_all()

    start = time.perf_counter()

    ingest_customer_csv(False)
    ingest_product_csv(False)
    ingest_rental_csv(False)

    elapsed = time.perf_counter() - start
    logger.info(f"db ingest executed in {elapsed:0.4f} seconds")
    print(f"db ingest executed in {elapsed:0.4f} seconds")

    # db_dict = show_available_products()

    # print(db_dict)

    # db_dict = show_rentals('P000002')

    # print(db_dict)
