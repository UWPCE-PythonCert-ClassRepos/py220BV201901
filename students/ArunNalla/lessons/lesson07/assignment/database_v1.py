#! usr/bin/env python3
""" Assignment Lesson05: MongoDB
    by Arun 02/18/2019"""

from pymongo import MongoClient
import logging
import csv
import os
import time
import asyncio

logging.basicConfig(level = logging.INFO)
# FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
# LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
# FORMATTER = logging.Formatter(FORMAT)

# FILE_HANDLER = logging.FileHandler(LOG_FILE)
# FILE_HANDLER.setFormatter(FORMATTER)
# FILE_HANDLER.setLevel(logging.INFO)

# CONSOLE_HANDLER = logging.StreamHandler()
# CONSOLE_HANDLER.setLevel(logging.DEBUG)
# CONSOLE_HANDLER.setFormatter(FORMATTER)

# LOGGER = logging.getLogger()
# LOGGER.addHandler(FILE_HANDLER)
# LOGGER.addHandler(CONSOLE_HANDLER)


try:
    client = MongoClient(host='localhost', port=27017) # make connection to MongoDB
    logging.info('Connection Success')
except Exception as error1:
    logging.error('Failed connection')

try:
    db = client['my_database'] # creat a database by connecting to MongoDB
    logging.info ('Database created')
except Exception as error2:
    logging.error('Failed to create database')

""" created collections: customer, product and rentals"""
try:
    c_customer = db['customer']
    c_product = db['product']
    c_rentals = db['rentals']
    logging.info (f'Collections successfully done')
except Exception as error3:
    logging.error("Unable to create collection")

client.close()

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
start_time = time.time()

async def import_data(data_dir, product, customer, rental):
    """Function to create three collections and add documents from CSV files"""
    start_time = time.time()
    added = []
    errors = []
    try:
        with open(os.path.join(data_dir, product), 'r') as file:
            header = next(csv.reader(file))
            logging.info(f'Header seprated from "{product}"')
            add = 0
            error = 0
            logging.info(f'Reading file: "{product}"')
            for row in csv.reader(file):
                c_product.insert_one({header[0] : row[0],
                                    header[1]:row[1],
                                    header[2]:row[2],
                                    header[3]:row[3]})
                if c_product.acknowledged:
                    add += 1
                else:
                    logging.warning(f'Error occured in reading "{row}" of "{product}"')
                    error += 1
                await asyncio.sleep(0)
            added.insert(0, add)
            errors.insert(0, error)
            logging.info(f'Succesfully added "{add}" documents with "{error}" errors to collection from "{product}"')

            print (time.time()-start_time, "Time to read product file")
    except FileNotFoundError:
        logging.error(f'{product} not in folder')
    except Exception as err2:
        logging.error(f'"{type(err2)}" occured reading: "{product}"')
    try:
        with open(os.path.join(data_dir, customer), 'r') as file:
            header = next(csv.reader(file))
            logging.info(f'Header seprated from "{customer}"')
            add = 0
            error = 0
            logging.info(f'Reading file: "{customer}"')
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
                    # insert_one method returns True or False
                    add += 1
                else:
                    logging.warning(f'Error occured in reading "{row}" of "{customer}"')
                    error += 1
                await asyncio.sleep(0)
            added.append(add)
            errors.append(error)
            logging.info(f'Succesfully added "{add}" documents with "{error}" errors to collection from "{customer}"')            
            print (time.time()- start_time, "Time take for reading customer file")
    except FileNotFoundError:
        logging.error(f'{customer} not in folder')
    except Exception as err:
        logging.error(f'"{type(err)}" occured reading : "{customer}"')

    try:
        with open(os.path.join(data_dir, rental), 'r') as file:
            header = next(csv.reader(file))
            logging.info(f'Header seprated from "{rental}"')
            add = 0
            error = 0
            logging.info(f'Reading file: "{rental}"')
            for row in csv.reader(file):
                c_rentals.insert_one({header[0] : row[0],
                                    header[1]:row[1], header[2]:row[2],
                                    header[3]:row[3], header[4]:row[4],
                                    header[5]:row[5]})
                if c_rentals.acknowledged:
                    add += 1
                else:
                    error += 1
                    logging.warning(f'Error occured in reading "{row}" of "{product}"')
                await asyncio.sleep(0)
            added.append(add)
            errors.append(error)
            
            logging.info(f'Succesfully added "{add}" documents with "{error}" errors'
            f'to collection from "{rental}"')
            print (time.time()-start_time, "time take for reading rental files")
    except FileNotFoundError:
        logging.error(f'{rental} not in folder')
    except Exception as err3:
        logging.error(f'"{type(err3)}" occured reading: "{rental}"')
    logging.info (f'Done with adding collections')
    await asyncio.gather()
    print (time.time()- start_time, "TOTAL TIME TAKEN")
    return (tuple(added), tuple(errors))

async def show_available_products():
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

def show_rentals(item=None):
    """Function to get the customer details by querying against the rental ID"""
    try:
        query = c_rentals.find({'product_id':item}, {'_id': 0, 'product_id': 0})
        logging.info(f'Querying customers renting a product : Started')
        item_rented = {}
        for i in query:
            key = i['user_id']
            del i['user_id']
            item_rented[key] = i
        logging.info(f'Querying cutomers renting a product : Ends')
        # await asyncio.sleep(0)
    except Exception as err5:
        logging.error(f'{type(err5)} occured during querying rentals')
    return item_rented

def del_coll():
    """Function to drop / delate all the collection from the database"""
    c_customer.drop()
    c_product.drop()
    c_rentals.drop()

    logging.info("Collection were deleted from database")

if __name__ == '__main__':
    del_coll()
    asyncio.run(import_data(DATA_DIR, 'products.csv', 'customers.csv', 'rentals.csv'))
    asyncio.run(show_available_products())
    show_rentals()
