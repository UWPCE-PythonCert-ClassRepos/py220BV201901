#! usr/bin/env python
""" Creating a customer database
by Arun Nalla 01/30/2019 Assignment 3"""

from peewee import *
import logging

logging.basicConfig(level=logging.INFO)

db = SqliteDatabase('customer.db')

class Customer(Model):
    """Customer class comprising a table 
    with all the custormer info"""

    customer_ID = CharField (primary_key=True, max_length=10, unique=True)
    customer_name = CharField(max_length = 30)
    customer_last_name = CharField(max_length=20)
    customer_address = CharField()
    customer_phone = CharField(max_length=15)
    customer_email = CharField(null=True)
    customer_status = CharField(max_length=10)
    customer_credit_limit = DecimalField(max_digits=5, decimal_places=2, auto_round=False)

    class Meta:
        """refernce to the database"""
        database = db
        logging.info ('Customer database has been generated')

    logging.info('Generated fields info for customer table')

def create_customer_table():
    """Function to create table"""
    db.connect()
    db.execute_sql('PRAGMA foreign_keys = ON;')
    Customer.create_table()
    logging.info('Created a new table / update existing database table')
    db.close()
    logging.info('Database is successfully closed')

def add_new_instance(*customer_data):
    """customer_id, name, lastname, home_address,
                    phone_number, email_address, status, credit_limit)"""
    """Function to add a new row/instance to the main table"""
    db.connect()
    logging.info('Database connect at add_instance level')
    try:
        with db.transaction():
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

            logging.info(f'New customer "{new_customer.customer_name}" with an\
            unique custome ID "{new_customer.customer_ID}" has been generated')
    except IntegrityError:
        logging.warning(f'Unable to create/update database)')
    db.close()

def search_customer(customer_id):
    '''Function to search a customer using customer_ID'''

    try:
        query = Customer.select().where(Customer.customer_ID == customer_id).get()
        logging.info(f'The customer_ID "{query.customer_ID}" corresponds to "{query.customer_name}"')
        data_dict = {}
        if query.customer_ID:
            data_dict = {}
            data_dict[query.customer_ID] = (query.customer_name,
                                        query.customer_last_name,
                                        query.customer_email,
                                        query.customer_phone)
            logging.info(f'Dict of queried ID "{query.customer_ID}" is\n{data_dict}')
        else:
            logging.info(f'{query.customer_ID} not found')
        return data_dict

    except DoesNotExist:
        logging.warning(f'The "{customer_id}" is not in the customer database')
        return {}

def delete_customer(cust_id_del):
    """Function to delete a single instance/row from the table"""
    try:
        query = Customer.select().where(Customer.customer_ID == cust_id_del).get()
        query.delete_instance()
        logging.info (f'Deleted "{query.customer_name}" with "{query.customer_email}" from the database')
    except DoesNotExist:
        logging.warning(f'The costumer with {cust_id_del} d\'not exits in the database')
    db.close()
    
def update_customer_credit(customer_id, cre_lim):
    ''' Function to update the customer credit limit'''
    try:
        query = Customer.select().where(Customer.customer_ID == customer_id).get()
        credit_limit_ID = query.customer_credit_limit
        if credit_limit_ID >= 0:
            query.customer_credit_limit = cre_lim 
            query.save()
            logging.info (f'Updated credit limit of {query.customer_name} from {credit_limit_ID} to {query.customer_credit_limit}')
        else:
            raise ValueError
            logging.warning(f'Credit limit of "{query.customer_name}" was not updated')

    except DoesNotExist:
        logging.warning(f'The "{customer_id}" doesn\'t exist in database')
    except ValueError:
        logging.warning(f'Credit limit of "{query.customer_name}" was not updated')

    db.close()

def list_active_customers():
    """Function to determine the number of active customers - count"""

    query = Customer.select().where(Customer.customer_status == 'active').count()
    logging.info (f'Total number of acitve customers are {query}')

if __name__ == '__main__':
    create_customer_table()
    logging.info('Table end')
