#! usr/bin/env python3
""" Assignment Lesson05: MongoDB
    by Arun 02/18/2019"""

import logging
import csv
import os
import time
import asyncio
import datetime
from pymongo import MongoClient

logging.basicConfig(level=logging.WARNING)

try:
    CLIENT = MongoClient(host='localhost', port=27017)

    logging.info('Connection Success')
except Exception as error1:
    logging.error('Failed connection')

try:
    DB = CLIENT['my_database']
    logging.info('Database created')
except Exception as error2:
    logging.error('Failed to create database')

""" created collections: customer, product and rentals"""
try:
    C_CUSTOMER = DB['customer']
    C_PRODUCT = DB['product']
    C_RENTALS = DB['rentals']
    logging.info(f'Collections successfully done')

except Exception as error3:
    logging.error("Unable to create collection")

CLIENT.close()

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

START_TIME = time.time()

print(datetime.datetime.now(), "CODE START TIME")

async def product_csv(file_name):
    """Function to read and update each row into product collection"""
    count_prior = C_PRODUCT.estimated_document_count()
    processed = []
    print(datetime.datetime.now(), "PRODUCT CSV READING START")
    try:
        with open(os.path.join(DATA_DIR, file_name), 'r') as file:
            header = next(csv.reader(file))
            logging.info(f'Header seprated from "{file_name}"')
            add = 0
            error = 0
            logging.info(f'Reading file: "{file_name}"')
            for row in csv.reader(file):
                C_PRODUCT.insert_one({header[0] : row[0],
                                      header[1] : row[1],
                                      header[2] : row[2],
                                      header[3] : row[3]})
                if C_PRODUCT.acknowledged:
                    add += 1
                else:
                    logging.warning(f'Error in reading "{row}" of "{file_name}"')
                    error += 1
            processed.append(add)
            logging.info(f'Succesfully added "{add}" documents with "{error}"errors to collection from "{file_name}"')
            count_new = C_PRODUCT.estimated_document_count()
        await asyncio.sleep(5)
        print(datetime.datetime.now(), "PRODUCT CSV READIND END")
        elapsed_time = (time.time() - START_TIME)
        return (processed[0], count_prior, count_new, elapsed_time)
    except FileNotFoundError:
        logging.error(f'{file_name} not in folder')
    except Exception as err2:
        logging.error(f'"{type(err2)}" occured reading: "{file_name}"')

async def customers_csv(file_name):
    """Function to read and update each row into customer collection"""
    count_prior = C_CUSTOMER.estimated_document_count()
    processed = []
    print(datetime.datetime.now(), "CUSTOMER CSV READING START")
    try:
        with open(os.path.join(DATA_DIR, file_name), 'r') as file:
            header = next(csv.reader(file))
            logging.info(f'Header seprated from "{file_name}"')
            add = 0
            error = 0
            logging.info(f'Reading file: "{file_name}"')
            for row in csv.reader(file):
                C_CUSTOMER.insert_one({header[0] : row[0],
                                       header[1] : row[1],
                                       header[2] : row[2],
                                       header[3] : row[3],
                                       header[4] : row[4],
                                       header[5] : row[5],
                                       header[6] : row[6],
                                       header[7] : row[7]})
                if C_CUSTOMER.acknowledged:
                    add += 1
                else:
                    logging.warning(f'Error occured in reading "{row}" of "{file_name}"')
                    error += 1
            processed.append(add)
            logging.info(f'Succesfully added "{add}" documents with "{error}" errors to collection from "{file_name}"')
            count_new = C_CUSTOMER.estimated_document_count()
        await asyncio.sleep(1)
        print(datetime.datetime.now(), "CUSTOMER CSV READING END")
        elapsed_time = (time.time()-START_TIME)
        return (processed[0], count_prior, count_new, elapsed_time)
    except FileNotFoundError:
        logging.error(f'{file_name} not in folder')
    except Exception as err:
        logging.error(f'"{type(err)}" occured reading : "{file_name}"')

async def rentals_csv(file_rent):
    """Function to read and update each row into rental collection"""
    rent_added, rent_errors = [], []
    count_prior = C_RENTALS.estimated_document_count()
    print(datetime.datetime.now(), "RENTAL CSV READING START")
    try:
        with open(os.path.join(DATA_DIR, file_rent), 'r') as file:
            header = next(csv.reader(file))
            logging.info(f'Header seprated from "{file_rent}"')
            add = 0
            error = 0
            logging.info(f'Reading file: "{file_rent}"')
            for row in csv.reader(file):
                C_RENTALS.insert_one({header[0] : row[0],
                                      header[1] : row[1],
                                      header[2] : row[2],
                                      header[3] : row[3],
                                      header[4] : row[4],
                                      header[5] : row[5]})
                if C_RENTALS.acknowledged:
                    add += 1
                else:
                    error += 1
                    logging.warning(f'Error occured in reading "{row}" of "{file_rent}"')
            await asyncio.sleep(0)
            print(datetime.datetime.now(), "RENTAL CSV READING END")
            rent_added.append(add)
            rent_errors.append(error)
            logging.info(f'Succesfully added "{add}" documents with "{error}" errors to collection from "{file_rent}"')
        elapsed_time = (time.time()-START_TIME)
        return (rent_added[0], count_prior, rent_added[0] - rent_errors[0], elapsed_time)
    except FileNotFoundError:
        logging.error(f'{file_rent} not in folder')
    except Exception as err3:
        logging.error(f'"{type(err3)}" occured reading: "{file_rent}"')

async def import_data(products, customers, rentals):
    """Function to create three collections and add documents from CSV files
    using async"""
    prod_task = asyncio.create_task(product_csv(products))
    cust_task = asyncio.create_task(customers_csv(customers))
    rent_task = asyncio.create_task(rentals_csv(rentals))
    output = await asyncio.gather(prod_task, cust_task, rent_task)
    print(datetime.datetime.now(), "RUN END TIME")
    print(tuple(output))
    return tuple(output[:-1])

async def show_available_products():
    """ Function to pull 'quering' out all prodcuts"""

    update_type = C_PRODUCT.update_many({'product_type': 'Livingroom'},
                                        {'$set' : {'product_type' : 'livingroom'}})
    logging.info('Updated Livingroom from Capitalise to lowercase. Updated' +
    f'"{update_type.modified_count}" collections.')

    try:
        query = C_PRODUCT.find({}, {'_id': 0, 'product_id': 1, 'description': 1,
                                    'product_type': 1, 'quantity_available': 1})
        logging.info(f'Querying for products started')
        products = {}
        for i in query:
            key = i['product_id']
            del i['product_id']
            products[key] = i
        logging.info(f'Querying products ends')
        await asyncio.sleep(1)
    except Exception as err4:
        logging.error(f'"{type(err4)}" occured during quering prodcuts')
    return products

async def show_rentals(item=None):
    """Function to get the customer details by querying against the rental ID"""
    try:
        query = C_RENTALS.find({'product_id':item}, {'_id': 0, 'product_id': 0})
        logging.info(f'Querying customers renting a product : Started')
        item_rented = {}
        for i in query:
            key = i['user_id']
            del i['user_id']
            item_rented[key] = i
        logging.info(f'Querying customers renting a product : Ends')
        await asyncio.sleep(1)
    except Exception as err5:
        logging.error(f'{type(err5)} occured during querying rentals')
    return item_rented

def del_coll():
    """Function to drop / delate all the collection from the database"""
    C_CUSTOMER.drop()
    C_PRODUCT.drop()
    C_RENTALS.drop()

    logging.info("Collection were deleted from database")

if __name__ == '__main__':
    del_coll()
    START_TIME = time.time()
    asyncio.run(import_data('products.csv', 'customers.csv', 'rentals.csv'))
    print(time.time()-START_TIME, ":Total Time take - Parallel")
    # asyncio.run(show_available_products())
    # asyncio.run(show_rentals('P000001'))

