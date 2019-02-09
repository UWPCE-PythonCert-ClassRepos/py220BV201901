"""
This is a test file to run the funcitons in basic_operations.py.
To see if the functions work well
"""

from basic_operations import *

#add new customer to database
add_customer()

#populate database with a group of records
dict_example_customers = {'002':["Lily", "Harmon", "Redmond WA", "111-111-1111", "Lily@gmail.com", 5000],
                    '003':["Jonathan", "Curtis", "Renton WA", "333-333-3333", 'Jon@gmail.com', 8888],
                    '004':["Tim", "Briest", "Seattle WA", "444-444-8888", 'tim@gmail.com', 6666]}
add_customers(dict_example_customers)

#search
search_customer('002')

#delete
delete_customer('001')

#update
update_customer_credit('002', '222222')

#add new sale, got datatype mismatch error on the foreign key field
dict_example_sales = {'CO01':['2019-01-01', False, '002'],
                        'CO02':['2019-02-02', True, '002'],
                        'CO03':['2019-02-03', True, '003']}

add_sales(dict_example_sales)

#count active customers
list_active_customer()