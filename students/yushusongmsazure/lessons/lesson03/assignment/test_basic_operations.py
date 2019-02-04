'''
Yushu Song
Assignment03
'''
import pytest
from basic_operations import *

CUSTOMER_ID = 12345
FIRST_NAME = 'Larry'
LAST_NAME = 'Page'
HOME_ADDRESS = 'Palo Alto, California'
PHONE_NUMBER = '650-329-2100'
EMAIL_ADDRESS = 'lpage@gmail.com'
STATUS = 0
CREDIT_LIMIT = 58766628.00

class TestBasicOperations():
    '''
    Test class for bassic_operations
    '''

    def test_init(self):
        '''
        Test init_db function
        '''
        init_db()

        # Check record for customer Kate Perry
        assert Customer.select().where(
            Customer.first_name == 'Kate' and
            Customer.last_name == 'Perry' and
            Customer.home_address == 'One Microsoft Way, Redmond, 98052' and
            Customer.email_address == 'kateperry@outlook.com' and
            Customer.phone_number == '425-595-8068' and
            Customer.status == 0 and
            Customer.credit_limit == 19818.98).count() == 1

        # Check record for customer Eric McCarthy
        assert Customer.select().where(
            Customer.first_name == 'Eric' and
            Customer.last_name == 'McCarthy' and
            Customer.home_address == '910 232nd PL NE, Sammamish, 98074' and
            Customer.email_address == 'emccarthy2009@gmail.com' and
            Customer.phone_number == '425-595-8068' and
            Customer.status == 1 and
            Customer.credit_limit == 200.0).count() == 1

    def test_add_customer(self):
        '''
        Test adding a customer
        '''
        add_customer(customer_id=CUSTOMER_ID,
                     first_name=FIRST_NAME,
                     last_name=LAST_NAME,
                     home_address=HOME_ADDRESS,
                     phone_number=PHONE_NUMBER,
                     email_address=EMAIL_ADDRESS,
                     status=STATUS,
                     credit_limit=CREDIT_LIMIT)

        assert Customer.select().where(
            Customer.customer_id == CUSTOMER_ID and
            Customer.first_name == FIRST_NAME and
            Customer.last_name == LAST_NAME and
            Customer.home_address == HOME_ADDRESS and
            Customer.email_address == EMAIL_ADDRESS and
            Customer.phone_number == PHONE_NUMBER and
            Customer.status == STATUS and
            Customer.credit_limit == CREDIT_LIMIT).count() == 1

    def test_search_customer(self):
        '''
        Test searching a customer given a customer ID
        '''
        customer = search_customer(CUSTOMER_ID)

        assert customer['customer_id'] == CUSTOMER_ID
        assert customer['first_name'] == FIRST_NAME
        assert customer['last_name'] == LAST_NAME
        assert customer['phone_number'] == PHONE_NUMBER
        assert customer['email'] == EMAIL_ADDRESS