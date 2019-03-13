import sys

from loguru import logger

from linear import linear
from parallel import parallel

from models import util_drop_all
from database import Connection
from database import show_rentals

# Standalone function to initialize logging
logger.add(sys.stdout, level='WARNING')
logger.add("logfile_{time}.txt", level='INFO')
logger.enable(__name__)

def main():
    """
    Ensure you application will create an empty database if one doesn’t exist
    when the app is first run. Call it customers.db
    """

    print("Start linear ingest from CSV files")

    ret_list_linear = linear()

    print("Start parallel ingest from CSV files")

    ret_list_parallel = parallel()

    print("CSV ingest completed")

    result = show_rentals('P000003')
    print(result)

    print("Linear ingest statistics:")
    for docstats in ret_list_linear:
        print(f"{docstats[0]} doc: num  records: {docstats[3]}")
        print(f"{docstats[0]} doc: time elapsed: {docstats[4]}")


    print("Parallel ingest statistics:")
    for docstats in ret_list_parallel:
        print(f"{docstats[0]} doc: num  records: {docstats[3]}")
        print(f"{docstats[0]} doc: time elapsed: {docstats[4]}")


if  __name__ == '__main__':
    main()
