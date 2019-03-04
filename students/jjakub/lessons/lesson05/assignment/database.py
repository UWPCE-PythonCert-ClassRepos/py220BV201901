# Database
# pylint: disable=too-many-locals
""""
Module to handle database operations
"""

import csv
import datetime
import logging
import sys
from pathlib import Path
from pymongo import MongoClient

MONGO = MongoClient(host='127.0.0.1', port=27017)
DB = MONGO['HPN_database']

PRDCT = DB["product"]
CUST = DB["customer"]
RNTL = DB["rental"]

DB.PRDCT.create_index("product_id")
DB.CUST.create_index("user_id")

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel("INFO")


def import_data(directory_name, product_file, customer_file, rental_file):
    """ import csv files into database """
    file_list = [product_file, customer_file, rental_file]
    for file in file_list:
        success_cnt, error_cnt = 0, 0
        try:
            data = open(Path(directory_name, file), "r", encoding="utf-8-sig")
            header = next(csv.reader(data))
            for row in csv.reader(data):
                if file == file_list[0]:
                    DB.PRDCT.insert_one({header[0]:row[0],
                                         header[1]:row[1],
                                         header[2]:row[2],
                                         header[3]:row[3]})
                    if DB.PRDCT.acknowledged:
                        success_cnt += 1
                        LOGGER.info("Item added to product collection: %s", row[0])
                    else:
                        error_cnt += 1
                        LOGGER.error("Prodcut collection insert error: %s", row[0])
                    prdct_success, prdct_error = success_cnt, error_cnt
                if file == file_list[1]:
                    DB.CUST.insert_one({header[0]:row[0],
                                        header[1]:row[1],
                                        header[2]:row[2],
                                        header[3]:row[3],
                                        header[4]:row[4],
                                        header[5]:row[5]})
                    if DB.CUST.acknowledged:
                        success_cnt += 1
                        LOGGER.info("Item added to customer collection: %s", row[0])
                    else:
                        error_cnt += 1
                        LOGGER.error("Customer collection insert error: %s", row[0])
                    cust_success, cust_error = success_cnt, error_cnt
                if file == file_list[2]:
                    DB.RNTL.insert_one({header[0]:row[0],
                                        header[1]:row[1]})
                    if DB.RNTL.acknowledged:
                        success_cnt += 1
                        LOGGER.info("Item added to rental collection: %s", row[0])
                    else:
                        error_cnt += 1
                        LOGGER.error("Rental collection insert error: %s", row[0])
                    rntl_success, rntl_error = success_cnt, error_cnt
        except FileNotFoundError:
            LOGGER.error("File does not exist: %s", Path(directory_name, file))
            sys.exit(1)
    return (prdct_success, cust_success, rntl_success), (prdct_error, cust_error, rntl_error)


def show_available_products():
    """ list products with available inventory """
    result = {}
    for doc in DB.PRDCT.find({"quantity_available": {"$gt": "0"}}):
        result[doc["product_id"]] = {"description" : doc["description"],
                                     "product_type" : doc["product_type"],
                                     "quantity_available" : doc["quantity_available"]}
    return result


def show_rentals(product_id):
    """ show information for customers that have rented a product """
    user_list, result = [], {}
    for doc in DB.RNTL.find({"product_id": product_id}):
        user_list.append(doc["user_id"])
    if user_list == []:
        LOGGER.info("Product ID not found: %s", product_id)
    else:
        for doc in DB.CUST.find({"user_id": {"$in": user_list}}):
            result[doc["user_id"]] = {"name" : doc["name"],
                                      "address" : doc["address"],
                                      "phone_number" : doc["phone_number"],
                                      "email" : doc["email"]}
            LOGGER.info("Customer data reported: %s", doc["user_id"])
    return result


def delete_all():
    """ delete all data from collections """
    prdct_result = DB.PRDCT.delete_many({})
    LOGGER.info("Items deleted from product collection: %s", prdct_result.deleted_count)
    cust_result = DB.CUST.delete_many({})
    LOGGER.info("Items deleted from customer collection: %s", cust_result.deleted_count)
    rntl_result = DB.RNTL.delete_many({})
    LOGGER.info("Items deleted from rental collection: %s", cust_result.deleted_count)
    return prdct_result.deleted_count, cust_result.deleted_count, rntl_result.deleted_count
