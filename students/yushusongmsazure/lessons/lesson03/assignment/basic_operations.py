'''
Yushu Song
Assignment03
'''

import logging
import random
from customer_db import DATABASE, Customer

LOGGER = logging.getLogger()
HANDLER = logging.StreamHandler()
FORMATTER = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)
LOGGER.setLevel(logging.INFO)

def init_db():
    '''
    Populate the DB with customer info
    '''
    DATABASE.create_tables([Customer])
    Customer.create(customer_id=random.randint(1, 1000),
                    first_name='Kate',
                    last_name='Perry',
                    home_address='One Microsoft Way, Redmond, 98052',
                    phone_number='425-595-8068',
                    email_address='kateperry@outlook.com',
                    status=0,
                    credit_limit=19818.98)
    Customer.create(customer_id=random.randint(1, 1000),
                    first_name='Eric',
                    last_name='McCarthy',
                    home_address='910 232nd PL NE, Sammamish, 98074',
                    phone_number='425-111-4567',
                    email_address='emccarthy2009@gmail.com',
                    status=1,
                    credit_limit=200.0)

def add_customer(**kwargs):
    '''
    Add a new customer to the Customers database.
    '''
    Customer.create(customer_id=kwargs['customer_id'],
                    first_name=kwargs['first_name'],
                    last_name=kwargs['last_name'],
                    home_address=kwargs['home_address'],
                    phone_number=kwargs['phone_number'],
                    email_address=kwargs['email_address'],
                    status=kwargs['status'],
                    credit_limit=kwargs['credit_limit'])

def search_customer(customer_id):
    '''
    Search for a customer based on customer ID
    '''
    customer_dict = {}
    customer = Customer.select().where(Customer.customer_id == customer_id).get()

    LOGGER.info(f'Found customer_id: {customer.customer_id}')

    if customer:
        customer_dict['customer_id'] = customer.customer_id
        customer_dict['first_name'] = customer.first_name
        customer_dict['last_name'] = customer.last_name
        customer_dict['phone_number'] = customer.phone_number
        customer_dict['email'] = customer.email_address

    LOGGER.info(f'len is {len(customer_dict)}')
    return customer_dict

def list_active_customers():
    '''
    List count of active customers
    '''
    return Customer.select().where(Customer.status == 1).count()

def delete_customer(customer_id):
    '''
    Delete a customer based on the customer ID
    '''
    Customer.delete().where(Customer.customer_id == customer_id)

def update_customer_credit(customer_id, new_credit_limit):
    '''
    Update a customer's credit limit
    '''
    LOGGER.info(f'{customer_id} needs to increase credit_limit to {new_credit_limit}')
    customer = Customer.select().where(Customer.customer_id == customer_id).get()

    if customer:
        LOGGER.info(f'Old credit_limit {customer.credit_limit}; new credit_limit {new_credit_limit}')
        customer.credit_limit = new_credit_limit
    else:
        LOGGER.warning(f'Not customer found for ID {customer_id}')
        raise ValueError

    LOGGER.info(f'Update credit successfully to {customer.credit_limit}')

def main():
    '''
    Main function
    '''
    init_db()
    customer_id = 12345
    new_credit_limit = 10000.00
    add_customer(customer_id=customer_id,
                 first_name='Larry',
                 last_name='Page',
                 home_address='Palo Alto, California',
                 phone_number='650-329-2100',
                 email_address='lpage@gmail.com',
                 status=0,
                 credit_limit=58766628.00)

    search_customer(customer_id)

    try:
        update_customer_credit(customer_id, new_credit_limit)
    except ValueError:
        print("No customer found for ID {customer_id}")

    list_active_customers()
    delete_customer(customer_id)

if __name__ == "__main__":
    main()
