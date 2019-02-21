#! usr/bin/env python
""" Refactored customer database
by Arun Nalla 02/16/2019 Assignment 4"""

import csv
import logging
from peewee import *
import time

logging.basicConfig(level=logging.INFO)
log_format = ("%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s")
formatter = logging.Formatter(log_format)


file_handler = logging.FileHandler('db.log', mode='w')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)

logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

db = SqliteDatabase('customer.db')

class Customer(Model):
    """Customer class comprising a table
    with all the custormer info"""

    customer_ID = CharField(primary_key=True, max_length=10)
    customer_name = CharField(max_length=30)
    customer_last_name = CharField(max_length=20)
    customer_address = CharField(max_length=100)
    customer_phone = CharField(max_length=15)
    customer_email = CharField(max_length=100)
    customer_status = CharField(max_length=10)
    customer_credit_limit = DecimalField(max_digits=5, decimal_places=2)
    logger.info('Assigned field names to Customer table.')

    class Meta:
        """refernce to the database"""
        database = db

def create_customer_table():
    """Function to create table"""
    db.connect()
    db.execute_sql('PRAGMA foreign_keys = ON;')
    db.create_tables([Customer])
    logger.info('Created a new table/update existing database table.')
    db.close()

def total_customer():
    """Function to determin total number of customer in the database"""
    total_count = Customer.select().count()
    return total_count

def add_customer(*customer_data):
    """customer_id, name, lastname, home_address,
                    phone_number, email_address, status, credit_limit)"""
    """Function to add a new row/instance to the main table"""

    try:
        with db.transaction():
            logger.info('Database connect at add_instance level')
            new_customer = Customer.create(
                customer_ID=customer_data[0],
                customer_name=customer_data[1],
                customer_last_name=customer_data[2],
                customer_address=customer_data[3],
                customer_phone=customer_data[4],
                customer_email=customer_data[5],
                customer_status=customer_data[6],
                customer_credit_limit=customer_data[7])
            new_customer.save()

            logger.info(f'New customer "{new_customer.customer_name}" eith customer ID "{new_customer.customer_ID}" has been generated')
    except IntegrityError:
        logger.warning(f'Unable to create/update database')
        db.close()
        logger.info('Database is close after adding customer to the table')

def convert_csv_dict(filename):
    """Function to convert data from the csv file to list comprsing of dict values"""
    try:
        with open(filename, 'r') as file:
            next(csv.reader(file))
            logger.info(f'Sucessfully opened and read data from "{filename}".')
            yield [row for row in csv.reader(file)]
            logger.info('Generator: CSV file is iterated')
    except FileNotFoundError:
        logger.warning('CSV file don\'t exist in current working folder.')
    except Exception as err:
        logger.warning(f'File {filename} unable to open due to {type(err)}.')

def add_customer_csv(input_data=None):
    """Function to add a new customers (row/instance) to the main table"""

    """Converting raw data either from csv (using convert_csv_dict function)
    or python data types in a dict"""
    try:
        if input_data == convert_csv_dict:
            customer_data = convert_csv_dict(filename)
            logger.info(f' Iterable: Using Generators: File type {type(customer_data)}')
    except TypeError:
        logger.warning(f'Check data type {type(customer_data)}.')
    try:
        with db.transaction():
            num_cust = total_customer() # Customer number before adding new customers
            try:
                for customer in next(customer_data):
                    new_customer = Customer.create(
                        customer_ID=customer[0],
                        customer_name=customer[1],
                        customer_last_name=customer[2],
                        customer_address=customer[3],
                        customer_phone=customer[4],
                        customer_email=customer[5],
                        customer_status=customer[6],
                        customer_credit_limit=customer[7])
                new_customer.save()
                logger.info(f'Added "{total_customer() - num_cust}"'
                ' customers to the {Customer} database.')
            except StopIteration:
                logger.info(f' Generator ended {customer_data}.')
    except IntegrityError:
        logger.warning(f'Rows/Customers already exists or Unable to create/update database.')

    logger.info(f'Number of customer in {Customer} database: "{total_customer()}".')

    db.close()

    logger.info('Database is successfully closed.')


def search_customer(customer_id):
    '''Function to search a customer using customer_ID'''
    try:
        query = Customer.select().where(Customer.customer_ID == customer_id).get()
        data_dict = {"name":query.customer_name, "lastname":query.customer_last_name,
            "email": query.customer_email, "phone_number":query.customer_phone}
        logger.info(f'Dict of queried ID "{query.customer_ID}" is\n{data_dict}')
        return data_dict

    except DoesNotExist:
        return {}
        logger.warning(f'The "{customer_id}" is not in the customer database')
    db.close()

def delete_customer(cust_id_del):
    """Function to delete a single instance/row from the table"""
    try:
        num_cust = total_customer()
        query = Customer.select().where(Customer.customer_ID == cust_id_del).get()
        query.delete_instance()
        logger.info(f'Deleted "{query.customer_name, query.customer_last_name.upper()}" from database.')
        logger.info(f'Number of customers updated from "{num_cust}" to "{total_customer()}".')
        return query not in Customer
    except DoesNotExist:
        logger.warning(f'The costumer with {cust_id_del} d\'not exits in the database')
    db.close()

def update_customer_credit(customer_id, cre_lim):
    ''' Function to update the customer credit limit'''
    try:
        query = Customer.select().where(Customer.customer_ID == customer_id).get()
        if query not in Customer:
            raise ValueError
            logger.error(f'"{customer_id}" not present in database')
        else:
            query.customer_credit_limit = cre_lim 
            query.save()
            logger.info (f'Updated credit limit of {query.customer_name} to {query.customer_credit_limit}')
    except DoesNotExist:
        logger.warning(f'The "{customer_id}" doesn\'t exist in database')
        raise ValueError
    db.close()

def list_active_customers():
    """Function to determine the number of active customers - count"""
    query = Customer.select().where(Customer.customer_status == 'active').count()
    return query
    logger.info(f'Total number of active customers are {query}.')

def clear_table():
    #Clean data
    db.connect()
    db.drop_tables([Customer])
    logger.info(f'The information in the {Customer} table has been dropped.')

if __name__ == '__main__':
    create_customer_table()
    filename = 'data_customer.csv'
    # t1  = time.time()
    # add_customer_csv(convert_csv_dict)
    # t2 = time.time()
    # print (t2-t1)
    # print (len(Customer))
    
