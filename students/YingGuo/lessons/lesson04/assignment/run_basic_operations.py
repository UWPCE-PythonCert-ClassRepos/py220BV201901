"""
This is a test file to run the funcitons in basic_operations.py.
To see if the functions work well
"""

from basic_operations import *

#populate database with a group of records
dict_example_customers = {'002':["Lily", "Harmon", "Redmond WA", "111-111-1111", "Lily@gmail.com", True, 5000],
                    '003':["Jonathan", "Curtis", "Renton WA", "333-333-3333", 'Jon@gmail.com', False, 8888],
                    '004':["Tim", "Briest", "Seattle WA", "444-444-8888", 'tim@gmail.com', True, 6666]}
_add_customers(dict_example_customers)

#search
_search_customers('002')

#delete
_delete_customers('001')

#update
_update_customer_credit('002', '222222')

#count active customers
_list_active_customers()

#upload csv file to database
add_customer_csv("customer")