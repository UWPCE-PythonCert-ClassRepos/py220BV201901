'''
Import module
'''
import random
from customer_db import DATABASE, Customer

def init_db():
    '''
    Populate the DB with customer info
    '''
    DATABASE.create_tables([Customer])
    Customer.create(customer_id=random.randint(0, 1000),
                    first_name='Kate',
                    last_name='Perry',
                    home_address='One Microsoft Way, Redmond, 98052',
                    phone_number='425-595-8068',
                    email_address='kateperry@outlook.com',
                    status=0,
                    credit_limit=19818.98)
    Customer.create(customer_id=random.randint(0, 1000),
                    first_name='Eric',
                    last_name='McCarthy',
                    home_address='910 232nd PL NE, Sammamish, 98074',
                    phone_number='425-595-8068',
                    email_address='emccarthy2009@gmail.com',
                    status=0,
                    credit_limit=200.0)

def main():
    '''
    Main function
    '''
    init_db()
    for customer in Customer.select():
        print(customer.first_name)


if __name__ == "__main__":
    main()