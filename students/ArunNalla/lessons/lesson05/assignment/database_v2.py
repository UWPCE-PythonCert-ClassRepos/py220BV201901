#! usr/bin/env python3
""" Assignment Lesson05: MongoDB
    by Arun 02/18/2019"""

from pymongo import MongoClient
import logging
import csv
import os
#ip = '192.168.0.13'

logging.basicConfig(level=logging.INFO)

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
    logging.error("Unable tp create collection")

client.close()

data_dir = os.path.dirname(os.path.abspath(__file__))

def import_data(data_dir, customer, product, rental):
    """Function to create three collections and add documents from CSV files"""
    added = []
    errors = []
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
            added.append(add)
            errors.append(error)
            logging.info(f'Succesfully added "{add}" documents with "{error}" errors to collection from "{customer}"')
    except FileNotFoundError:
        logging.error(f'{customer} not in folder')
    except Exception as err:
        logging.error(f'"{type(err)}" occured reading : "{customer}"')

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
            added.insert(0, add)
            errors.insert(0, error)
            logging.info(f'Succesfully added "{add}" documents with "{error}" errors to collection from "{product}"')
    except FileNotFoundError:
        logging.error(f'{product} not in folder')
    except Exception as err2:
        logging.error(f'"{type(err2)}" occured reading: "{product}"')

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
                if c_customer.acknowledged:
                    add += 1
                else:
                    error += 1
                    logging.warning(f'Error occured in reading "{row}" of "{product}"')
            added.append(add)
            errors.append(error)
            logging.info(f'Succesfully added "{add}" documents with "{error}" errors'
            f'to collection from "{rental}"')
    except FileNotFoundError:
        logging.error(f'{rental} not in folder')
    except Exception as err3:
        logging.error(f'"{type(err3)}" occured reading: "{rental}"')

    logging.info (f'Done with adding collections')
    return (tuple(added), tuple(errors))

def show_available_products():
    """ Function to pull 'quering' out all prodcuts"""
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
    except Exception as err5:
        logging.error(f'{type(err5)} occured during querying rentals')
    return item_rented

def del_coll():
    """Function to drop / delate all the collection from the database"""
    c_customer.drop()
    c_product.drop()
    c_rentals.drop()

if __name__ == '__main__':
    del_coll()
    import_data(data_dir, 'customer.csv', 'product.csv', 'rental.csv')
    show_available_products()
    show_rentals()

