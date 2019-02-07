
import peewee
import csv
from basic_operations import *
from create_database import *


def query():
    # for cust in Customer.select().where(Customer.customer_id == 'test_customer_id'):
    #     print(cust)

    # add_customer('test_customer_id', 'test_name', 'test_last_name', 'test_address', 'test_phone_number', 'test_email', 'test_status', 000)

    # cust_dict = Customer.select().where(Customer.customer_id == 'test_001')
    # print(cust_dict)
    update_cust = Customer.update(credit_limit= 555).where(Customer.customer_id == 'no')
    print(update_cust)

    # cust_dict = Customer.select().dicts().where(Customer.customer_id == 'test_001')[0]
    # print(cust_dict)


    # cust_dict = search_customer('test_001')
    # print(cust_dict)

    # cust_dict = Customer.select().dicts().where(Customer.customer_id == 'test_009')[0]
    # print(cust_dict)

    # delete_customer('test_customer_id')

    # remove_cust = Customer.delete().where(Customer.customer_id == 'no_customer')


    # for x in Customer.select():
    #     print(x.name)

# for cust in Customer.select().dicts().where(Customer.name == 'Bill'):
#     print(cust)

    # for cust in Customer.select().dicts().where(Customer.customer_id == 'test_001'):
    #     print(cust)

# cust_dict = {}
# cust_dict = Customer.select().dicts().where(Customer.customer_id == 'C000662')

# for i in cust_dict:
#     print(i)

if __name__ == "__main__":
    query()