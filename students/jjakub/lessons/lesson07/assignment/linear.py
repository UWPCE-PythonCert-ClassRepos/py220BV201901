# Linear

""""
Module to handle linear database operations
"""

import cProfile
import csv
import datetime
import os
import sys
from pathlib import Path
# pylint: disable=unused-import
from database import DB, PRDCT, CUST, RNTL, LOGGER
# pylint: enable=unused-import


def import_data(directory_name, product_file, customer_file, rental_file):
    """ run database load tasks in linear sequence """
    import_product(directory_name, product_file)
    import_customer(directory_name, customer_file)
    import_rental(directory_name, rental_file)


def import_product(directory_name, product_file):
    """ import product file into database """
    success_cnt, error_cnt, prev_cnt, curr_cnt = 0, 0, 0, 0
    start_prdct = datetime.datetime.now()
    prev_cnt = DB.PRDCT.count_documents({})

    try:
        data = open(Path(directory_name, product_file), "r", encoding="utf-8-sig")
        header = next(csv.reader(data))
        for row in csv.reader(data):

            DB.PRDCT.insert_one({header[0]:row[0],
                                 header[1]:row[1],
                                 header[2]:row[2],
                                 header[3]:row[3]})

            if DB.PRDCT.acknowledged:
                success_cnt += 1
                LOGGER.debug("Item added to product collection: %s", row[0])
            else:
                error_cnt += 1
                LOGGER.error("Prodcut collection insert error: %s", row[0])

    except FileNotFoundError:
        LOGGER.error("File does not exist: %s", Path(directory_name, product_file))
        sys.exit(1)

    curr_cnt = DB.PRDCT.count_documents({})
    end_prdct = datetime.datetime.now()

    result = (success_cnt, prev_cnt, curr_cnt, end_prdct - start_prdct)
    LOGGER.info("Product result: %s", result)
    LOGGER.info("Product load: start time %s, end time %s", start_prdct, end_prdct)

    return result


def import_customer(directory_name, customer_file):
    """ import customer file into database """
    success_cnt, error_cnt, prev_cnt, curr_cnt = 0, 0, 0, 0
    start_cust = datetime.datetime.now()
    prev_cnt = DB.CUST.count_documents({})

    try:
        data = open(Path(directory_name, customer_file), "r", encoding="utf-8-sig")
        header = next(csv.reader(data))
        for row in csv.reader(data):

            DB.CUST.insert_one({header[0]:row[0],
                                header[1]:row[1],
                                header[2]:row[2],
                                header[3]:row[3],
                                header[4]:row[4],
                                header[5]:row[5],
                                header[6]:row[6],
                                header[7]:row[7]})

            if DB.CUST.acknowledged:
                success_cnt += 1
                LOGGER.debug("Item added to customer collection: %s", row[0])
            else:
                error_cnt += 1
                LOGGER.error("Customer collection insert error: %s", row[0])

    except FileNotFoundError:
        LOGGER.error("File does not exist: %s", Path(directory_name, customer_file))
        sys.exit(1)

    curr_cnt = DB.CUST.count_documents({})
    end_cust = datetime.datetime.now()

    result = (success_cnt, prev_cnt, curr_cnt, end_cust - start_cust)
    LOGGER.info("Customer result: %s", result)
    LOGGER.info("Customer load: start time %s, end time %s", start_cust, end_cust)

    return result


def import_rental(directory_name, rental_file):
    """ import rental file into database """
    success_cnt, error_cnt, prev_cnt, curr_cnt = 0, 0, 0, 0
    start_rntl = datetime.datetime.now()
    prev_cnt = DB.RNTL.count_documents({})

    try:
        data = open(Path(directory_name, rental_file), "r", encoding="utf-8-sig")
        header = next(csv.reader(data))
        for row in csv.reader(data):

            DB.RNTL.insert_one({header[0]:row[0],
                                header[1]:row[1],
                                header[2]:row[2],
                                header[3]:row[3],
                                header[4]:row[4],
                                header[5]:row[5]})

            if DB.RNTL.acknowledged:
                success_cnt += 1
                LOGGER.debug("Item added to rental collection: %s", row[0])
            else:
                error_cnt += 1
                LOGGER.error("Rental collection insert error: %s", row[0])

    except FileNotFoundError:
        LOGGER.error("File does not exist: %s", Path(directory_name, rental_file))
        sys.exit(1)

    curr_cnt = DB.RNTL.count_documents({})
    end_rntl = datetime.datetime.now()

    result = (success_cnt, prev_cnt, curr_cnt, end_rntl - start_rntl)
    LOGGER.info("Rental result: %s", result)
    LOGGER.info("Rental load: start time %s, end time %s", start_rntl, end_rntl)

    return result


def delete_all():
    """ delete all data from collections """
    prdct_result = DB.PRDCT.delete_many({})
    cust_result = DB.CUST.delete_many({})
    rntl_result = DB.RNTL.delete_many({})

    LOGGER.info("Items deleted from product collection: %s", prdct_result.deleted_count)
    LOGGER.info("Items deleted from customer collection: %s", cust_result.deleted_count)
    LOGGER.info("Items deleted from rental collection: %s", rntl_result.deleted_count)
    return prdct_result.deleted_count, cust_result.deleted_count, rntl_result.deleted_count


def drop_all():
    """ delete all data from collections """
    DB.PRDCT.drop()
    DB.CUST.drop()
    DB.RNTL.drop()

if __name__ == "__main__":
    # Get current path
    DATA_DIR = os.path.dirname(os.path.abspath(__file__))

    # Configure and enable internal profiling
    PR = cProfile.Profile()
    PR.enable()

    # Start linear operations and measure total module run time
    START_TIME = datetime.datetime.now()
    import_data(DATA_DIR, 'products.csv', 'customers.csv', 'rentals.csv')
    END_TIME = datetime.datetime.now()

    # Log results of module run time
    LOGGER.info("Total module run time: %s", END_TIME - START_TIME)
    LOGGER.info("Module: start time %s, end time %s", START_TIME, END_TIME)

    # Disable internal profiling and return results
    PR.disable()
    PR.print_stats()
    drop_all()

