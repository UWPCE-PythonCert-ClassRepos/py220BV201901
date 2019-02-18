#! usr/bin/env python
""" Creating a customer database
by Arun Nalla 01/30/2019 Assignment 3"""

import logging
from peewee import *
import csv


logging.basicConfig(level=logging.INFO)

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

    class Meta:
        """refernce to the database"""
        database = db
    logging.info('Generated Customer database')

def create_customer_table():
    """Function to create table"""
    db.connect()
    db.execute_sql('PRAGMA foreign_keys = ON;')
    Customer.create_table()
    logging.info('Created a new table/update an existing table')
    db.close()
    logging.info('Database is successfully closed')

def add_customer(*customer_data):
    """customer_id, name, lastname, home_address,
                    phone_number, email_address, status, credit_limit)"""
    """Function to add a new row/instance to the main table"""

    try:
        with db.transaction():
            logging.info('Database connect at add_instance level')
            new_customer = Customer.create(
                customer_ID=customer_data[0],
                customer_name=customer_data[1],
                customer_last_name=customer_data[2],                    customer_address=customer_data[3],
                customer_phone=customer_data[4],
                customer_email=customer_data[5],
                customer_status=customer_data[6],
                customer_credit_limit=customer_data[7])
            new_customer.save()

            logging.info(f'New customer "{new_customer.customer_name}" eith customer ID "{new_customer.customer_ID}" has been generated')
    except IntegrityError:
        logging.warning(f'Unable to create/update database')
        db.close()
        logging.info('Database is close after adding customer to the table')

def add_new_instance_csv(filename):
    """Function to convert data from the file to list comprsing of dict values"""
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            logging.info(f'Sucessfully opened and read data from "{filename}".')
            for row in reader:
                add_customer(*row)
        logging.info(f'Added customers to the {Customer} database.')

    except FileNotFoundError:
        logging.warning('CSV file don\'t exist in current working folder.')
    except TypeError:
        logging.warning(f'File {filename} unable to open.')

    logging.info(f'Number of customer in {Customer} database: "{len(Customer)}".')
    db.close()
    logging.info('Database is successfully closed.')


def search_customer(customer_id):
    '''Function to search a customer using customer_ID'''
    try:
        query = Customer.select().where(Customer.customer_ID == customer_id).get()
        data_dict = {"name":query.customer_name, "lastname":query.customer_last_name,
            "email": query.customer_email, "phone_number":query.customer_phone}
        logging.info(f'Dict of queried ID "{query.customer_ID}" is\n{data_dict}')

        return data_dict

    except DoesNotExist:
        return {}
        logging.warning(f'The "{customer_id}" is not in the customer database')
    db.close()

def delete_customer(cust_id_del):
    """Function to delete a single instance/row from the table"""
    try:
        query = Customer.select().where(Customer.customer_ID == cust_id_del).get()
        query.delete_instance()

        logging.info (f'Deleted "{query.customer_name}" with "{query.customer_email}" from the database')
        return query not in Customer
    except DoesNotExist:
        logging.warning(f'The costumer with {cust_id_del} d\'not exits in the database')
    db.close()
    
def update_customer_credit(customer_id, cre_lim):
    ''' Function to update the customer credit limit'''
    try:
        query = Customer.select().where(Customer.customer_ID == customer_id).get()
        if query not in Customer:
            raise ValueError
            logging.error(f'"{customer_id}" not present in database')
        else:
            query.customer_credit_limit = cre_lim 
            query.save()
            logging.info (f'Updated credit limit of {query.customer_name} to {query.customer_credit_limit}')
    except DoesNotExist:
        logging.warning(f'The "{customer_id}" doesn\'t exist in database')
        raise ValueError
    db.close()


def list_active_customers():
    """Function to determine the number of active customers - count"""

    query = Customer.select().where(Customer.customer_status == 'active').count()
    return query
    logging.info (f'Total number of acitve customers are {query}')

def clear_table():
    #Clean data
    db.connect()
    db.drop_tables([Customer])
    logging.info(f'The inforation in the {Customer} table has been dropped')
    db.close()



if __name__ == '__main__':
    create_customer_table()
    filename = 'customer.csv'
    



