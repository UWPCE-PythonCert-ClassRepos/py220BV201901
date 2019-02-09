'''
Yushu Song
Assignment03
'''
import pytest
from basic_operations import *
from customer_db import DATABASE

CUSTOMER_ID = 12345
FIRST_NAME = 'Larry'
LAST_NAME = 'Page'
HOME_ADDRESS = 'Palo Alto, California'
PHONE_NUMBER = '650-329-2100'
EMAIL_ADDRESS = 'lpage@gmail.com'
STATUS = 0

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
        credit_limit = 1500.0
        add_customer(customer_id=CUSTOMER_ID,
                     first_name=FIRST_NAME,
                     last_name=LAST_NAME,
                     home_address=HOME_ADDRESS,
                     phone_number=PHONE_NUMBER,
                     email_address=EMAIL_ADDRESS,
                     status=STATUS,
                     credit_limit=credit_limit)

        assert Customer.select().where(
            Customer.customer_id == CUSTOMER_ID and
            Customer.first_name == FIRST_NAME and
            Customer.last_name == LAST_NAME and
            Customer.home_address == HOME_ADDRESS and
            Customer.email_address == EMAIL_ADDRESS and
            Customer.phone_number == PHONE_NUMBER and
            Customer.status == STATUS and
            Customer.credit_limit == credit_limit).count() == 1

    def test_search_customer_exist(self):
        '''
        Test searching an existing customer given a customer ID
        '''
        customer = search_customer(CUSTOMER_ID)

        assert customer['customer_id'] == CUSTOMER_ID
        assert customer['first_name'] == FIRST_NAME
        assert customer['last_name'] == LAST_NAME
        assert customer['phone_number'] == PHONE_NUMBER
        assert customer['email'] == EMAIL_ADDRESS

    def test_search_customer_nonexist(self):
        '''
        Test searching a non customer given a customer ID
        '''
        customer = search_customer(0)
        assert not customer

    def test_list_active_customers(self):
        '''
        Test listing active customers
        '''
        assert Customer.select().where(Customer.status == 1).count() == 1

    # def test_update_customer_credit_succeed(self):
    #     '''
    #     Test listing active customers
    #     '''
    #     new_credit = 20000.0

    #     update_customer_credit(CUSTOMER_ID, new_credit)

    #     updated_credit_limit = Customer.select().where(
    #         Customer.customer_id == CUSTOMER_ID).get().credit_limit
    #     print(f'Updated: {update_customer_credit}')
    #     assert updated_credit_limit == new_credit

    # def test_delete_customer(self):
    #     '''
    #     Test deleting a customer give a customer ID
    #     '''
    #     Customer.delete().where(Customer.customer_id == CUSTOMER_ID)
    #     customer = search_customer(CUSTOMER_ID)
    #     assert not customer

    def clean_up(self):
        '''
        Clean up Customer table after testing
        '''
        clean_up_customer_db()
