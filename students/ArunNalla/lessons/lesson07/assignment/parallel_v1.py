#! usr/bin/env python3
""" Assignment Lesson05: MongoDB
    by Arun 02/18/2019"""

import logging
from pymongo import MongoClient
import csv
import os
import time
import datetime
import asyncio

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
logging.basicConfig(level=logging.WARNING, format=log_format)

def mongo_connection():

    try:
        client = MongoClient(host='localhost', port=27017) # make connection to MongoDB
        logging.info('Connection Success')
        return client
    except Exception as error1:
        logging.error('Failed connection')
    finally:
        client.close()

# try:
#     db = client['my_database'] # creat a database by connecting to MongoDB
#     logging.info ('Database created')
# except Exception as error2:
#     logging.error('Failed to create database')

#     """ created collections: customer, product and rentals"""
# try:
#     c_customer = db['customer']
#     c_product = db['product']
#     c_rentals = db['rentals']
#     logging.info (f'Collections successfully done')
# except Exception as error3:
#     logging.error("Unable to create collection")

# # client.close()

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

start_time = time.time()

async def product_csv(file_name):
    # prod_added, prod_errors = [], []
    mongo = mongo_connection()
    db = mongo['my_new_database']
    c_product = db['product']
    
    count_prior = c_product.estimated_document_count()
    processed = []
    try:
        with open(os.path.join(DATA_DIR, file_name), 'r') as file:
            header = next(csv.reader(file))
            logging.info(f'Header seprated from "{file_name}"')
            add = 0
            error = 0
            logging.info(f'Reading file: "{file_name}"')
            for row in csv.reader(file):
                c_product.insert_one({header[0] : row[0],
                                      header[1]:row[1],
                                      header[2]:row[2],
                                      header[3]:row[3]})
                if c_product.acknowledged:
                    add += 1
                else:
                    logging.warning(f'Error occured in reading "{row}" of "{file_name}"')
                    error += 1
            processed.append(add)
            # prod_added.insert(0, add)
            # prod_errors.insert(0, error)
            logging.info(f'Succesfully added "{add}" documents with "{error}" errors to collection from "{file_name}"')
            count_new = c_product.estimated_document_count()
        await asyncio.sleep(0)
        elapsed_time = (time.time() - start_time)
        # print (elapsed_time, "Time to complete product file")
        # return (prod_added[0], prod_errors[0])
        return (processed[0], count_prior, count_new, elapsed_time)
    except FileNotFoundError:
        logging.error(f'{file_name} not in folder')
    except Exception as err2:
        logging.error(f'"{type(err2)}" occured reading: "{file_name}"')

async def customers_csv(file_name):
    # cust_added, cust_errors = [], []
    mongo = mongo_connection()
    db = mongo['my_new_database']
    c_customer = db['customer']
    count_prior = c_customer.estimated_document_count()
    processed = []
    try:
        with open(os.path.join(DATA_DIR, file_name), 'r') as file:
            header = next(csv.reader(file))
            logging.info(f'Header seprated from "{file_name}"')
            add = 0
            error = 0
            logging.info(f'Reading file: "{file_name}"')
            for row in csv.reader(file):
                c_customer.insert_one({header[0]:row[0],
                                      header[1]:row[1],
                                      header[2]:row[2],
                                      header[3]:row[3],
                                      header[4]:row[4],
                                      header[5]:row[5],
                                      header[6]:row[6],
                                      header[7]:row[7]})
                if c_customer.acknowledged:
                    add += 1
                else:
                    logging.warning(f'Error occured in reading "{row}" of "{file_name}"')
                    error += 1
            processed.append(add)
            # cust_added.append(add)
            # cust_errors.append(error)
            logging.info(f'Succesfully added "{add}" documents with "{error}" errors to collection from "{file_name}"')
            count_new = c_customer.estimated_document_count()
        await asyncio.sleep(0)
        elapsed_time = (time.time()-start_time)
        # print (elapsed_time, "Time taken for reading customer file")
        # return (cust_added[0], cust_errors[0])
        return (processed[0], count_prior, count_new, elapsed_time)
    except FileNotFoundError:
        logging.error(f'{file_name} not in folder')
    except Exception as err:
        logging.error(f'"{type(err)}" occured reading : "{file_name}"')

async def rentals_csv(file_rent):
    mongo = mongo_connection()
    db = mongo['my_new_database']
    c_rentals = db['rentals']
    rent_added, rent_errors = [], []
    count_prior = c_rentals.estimated_document_count()
    try:
        with open(os.path.join(DATA_DIR, file_rent), 'r') as file:
            header = next(csv.reader(file))
            logging.info(f'Header seprated from "{file_rent}"')
            add = 0
            error = 0
            logging.info(f'Reading file: "{file_rent}"')
            for row in csv.reader(file):
                c_rentals.insert_one({header[0] : row[0],
                                    header[1]:row[1], header[2]:row[2],
                                    header[3]:row[3], header[4]:row[4],
                                    header[5]:row[5]})
                if c_rentals.acknowledged:
                    add += 1
                else:
                    error += 1
                    logging.warning(f'Error occured in reading "{row}" of "{file_rent}"')
            await asyncio.sleep(0)
            rent_added.append(add)
            rent_errors.append(error)
            logging.info(f'Succesfully added "{add}" documents with "{error}" errors'
            f'to collection from "{file_rent}"')            
        elapsed_time= (time.time()-start_time)
        # print (elapsed_time, 'Time taken for reading rental file')
        return (rent_added[0], count_prior, rent_added[0] - rent_errors[0], elapsed_time )
    except FileNotFoundError:
        logging.error(f'{file_rent} not in folder')
    except Exception as err3:
        logging.error(f'"{type(err3)}" occured reading: "{file_rent}"')

async def import_data(DATA_DIR, products, customers, rentals):
    """Function to create three collections and add documents from CSV files"""
    prod_loop = asyncio.create_task(product_csv(products))
    cust_loop = asyncio.create_task(customers_csv(customers))
    rent_loop = asyncio.create_task(rentals_csv(rentals))
    final_result = await asyncio.gather(prod_loop, cust_loop, rent_loop)
    print (tuple(final_result))
    elapsed_final_time = time.time()-start_time
    print (elapsed_final_time, "TOTAL TIME")
    return (tuple(final_result))

async def show_available_products():
    mongo = mongo_connection()
    db = mongo['my_new_database']
    c_product = db['product']
    """ Function to pull 'quering' out all prodcuts"""

    update_type = c_product.update_many({'product_type': 'Livingroom'},
                        {'$set' : {'product_type':'livingroom'}})
    logging.info('Updated Livingroom from Capitalise to lowercase.' + 
    f' Updated "{update_type.modified_count}" collections.')

    try:
        query = c_product.find({}, {'_id': 0, 'product_id': 1, 'description': 1,
                                    'product_type': 1, 'quantity_available': 1})
        logging.info(f'Querying for products started')
        products = {}
        for i in query:
            key = i['product_id']
            del i['product_id']
            products[key] = i
        logging.info(f'Querying products ends')
        await asyncio.sleep(0)
    except Exception as err4:
        logging.error(f'"{type(err4)}" occured during quering prodcuts')
    return products

async def show_rentals(item=None):
    """Function to get the customer details by querying against the rental ID"""
    mongo = mongo_connection()
    db = mongo['my_new_database']
    c_rentals = db['rentals']
    try:
        query = c_rentals.find({'product_id':item}, {'_id': 0, 'product_id': 0})
        logging.info(f'Querying customers renting a product : Started')
        item_rented = {}
        for i in query:
            key = i['user_id']
            del i['user_id']
            item_rented[key] = i
        logging.info(f'Querying cutomers renting a product : Ends')
        await asyncio.sleep(0)
    except Exception as err5:
        logging.error(f'{type(err5)} occured during querying rentals')
    return item_rented

def del_coll():
    """Function to drop / delate all the collection from the database"""
    mongo = mongo_connection()
    db = mongo['my_new_database']
    c_product = db['product']
    c_customer = db['customer']
    c_rentals = db['rentals']
    c_customer.drop()
    c_product.drop()
    c_rentals.drop()

    logging.info("Collection were deleted from database")

if __name__ == '__main__':
    del_coll()
    asyncio.run(import_data(DATA_DIR, 'products.csv', 'customers.csv', 'rentals.csv'))
    # asyncio.run(show_available_products())
    # asyncio.run(show_rentals('P000001'))

