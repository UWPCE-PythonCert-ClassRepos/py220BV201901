'''
Create customers database 'customers.db'.
Add/search/update/delete/list data in customers.db.
'''

from customers_model import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_database(*args):
    ''' Create customers database 'customers.db' '''
    logger.info('Build class Customers from the model in the database\n')

    database.create_tables([Customers])
    database.close()


def add_customer(*args):
    ''' Add customer to customers database '''
    logger.info(f'Adding customer to database: {args[0]}')

    customer = args[0]

    CUSTOMER_ID = 0
    FIRST_NAME = 1
    LAST_NAME = 2
    HOME_ADDR = 3
    PHONE = 4
    EMAIL = 5
    STATUS = 6
    CRED_LIMIT = 7

    try:
        with database.transaction():
            new_cust = Customers.create(
                customer_id=customer[CUSTOMER_ID],
                first_name=customer[FIRST_NAME],
                last_name=customer[LAST_NAME],
                home_addr=customer[HOME_ADDR],
                phone=customer[PHONE],
                email=customer[EMAIL],
                status=customer[STATUS],
                cred_limit=customer[CRED_LIMIT])
            new_cust.save()

            logger.info('Database add successful\n')
    except Exception as e:
        logger.info(f'Error creating Customer ID: {customer[CUSTOMER_ID]}')
        logger.info('It must already be in the database?\n')

    database.close()


def search_customer(*args):
    ''' Search for customer in customers database '''
    logger.info(f'Searching for customer in database: {args[0]}')

    cust_id = args[0]

    try:
        search_cust = Customers.get(Customers.customer_id == cust_id)
        return_cust = {
            'first_name': search_cust.first_name,
            'last_name': search_cust.last_name,
            'email': search_cust.email,
            'phone': search_cust.phone}
    except Exception as e:
        return_cust = {}
        logger.info(f'Error searching Customer ID: {cust_id}')
        logger.info('It must not be in the database?\n')

    logger.info('Here is the customer found:')
    logger.info(f'{return_cust}\n')

    return return_cust

    database.close()


def delete_customer(*args):
    ''' Delete customer from customers database '''
    logger.info(f'Deleting customer from database: {args[0]}')

    cust_id = args[0]

    try:
        cust_to_delete = Customers.get(Customers.customer_id == cust_id)
        cust_to_delete.delete_instance()

        logger.info('Database delete successful\n')
    except Exception as e:
        logger.info(f'Error deleting Customer ID: {cust_id}')
        logger.info('It must not be in the database?\n')

    database.close()


def update_customer(*args):
    ''' Update customer record in customers database '''
    logger.info(f'Search and update customers record: {args[0]}')

    cust_id = args[0]
    update_type = args[1]

    try:
        search_cust = Customers.get(Customers.customer_id == cust_id)

        if update_type == 'status':
            search_cust.status = args[2]
        else:
            search_cust.cred_limit = args[2]

        search_cust.save()

        logger.info('Record update successful\n')
    except Exception as e:
        logger.info(f'Error searching Customer ID: {cust_id}')
        logger.info('It must not be in the database?\n')

    database.close()


def list_customers(*args):
    ''' Count active customers in customers database '''
    logger.info('Counting active customers in the database')

    count_cust = 0

    try:
        for customer in Customers:
            if customer.status:
                count_cust += 1
    except Exception as e:
        count_cust = 0
        logger.info(f'No active customers found\n')

    logger.info(f'Here is the count of active customers: {count_cust}\n')

    return count_cust

    database.close()


def show_customers(*args):
    ''' Show all customers in the customers database '''
    logger.info('Read and print all customers records:')

    for customer in Customers:
        logger.info(f'ID:{customer.customer_id}, FN:{customer.first_name}, ' +\
                    f'LN:{customer.last_name}, AD:{customer.home_addr}, ' +\
                    f'PH:{customer.phone}, EM:{customer.email}, ' +\
                    f'ST:{customer.status}, CR:{customer.cred_limit}')

    print()
