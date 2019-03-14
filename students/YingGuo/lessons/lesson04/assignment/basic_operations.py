"""
hw4, requirements:
Using comprehensions, iterators / iterables, and generators appropriately,
and the instructor-provided customer data,
write data to your customer database and read / display it.
Verify existing unit tests still function correctly.
If necessary, update your tests to show the data is being maintained correctly in the database.
Add code to log all database data changes (adds, amends, deletes) to a file called db.log
"""

import logging
import csv
from decimal import Decimal
from management_database_model import *

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

#def add_customer(customer):
#    add_many_customers([customer])

def _add_customers(new_customer_list):
    """
    add a list of lists of new customer record to database Customer table
    (customer_id, name, lastname, home_address, phone_number,
    email_address, status, credit_limit.)
        return [
        ("123", "Name", "Lastname", "Address", "phone", "email", "active", 999),
        ("456", "Name", "Lastname", "Address", "phone", "email", "inactive", 10),
        ("123", "Name", "Lastname", "Address", "phone", "email", "active", 999),
        ("789", "Name", "Lastname", "Address", "phone", "email", "active", 0),
        ("345", "Name", "Lastname", "Address", "phone", "email", "active", -10),
        ("0123", "Name", "Lastname", "Address", "phone", "email", "active", 999),
        ("777", "Name", "Lastname", "Address", "phone", "email", "active", 999)
    ]
    """
    logging.info("connect to data base")
    database = SqliteDatabase('customer.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    logging.info("getting data from a list")

    for data in new_customer_list:
        user_input_1 = data[0]
        user_input_2 = data[1]
        user_input_3 = data[2]
        user_input_4 = data[3]
        user_input_5 = data[4]
        user_input_6 = data[5]
        if data[6] == "Active" or data[6] == "active":
            user_input_7 = True
        if data[6] == "Inactive" or "inactive":
            user_input_7 = False
        user_input_8 = data[7]
        try:
            with database.transaction():
                a_class_instance = Customer.create(
                    customer_id=user_input_1,
                    name=user_input_2,
                    last_name=user_input_3,
                    home_address=user_input_4,
                    phone_number=user_input_5,
                    email_address=user_input_6,
                    status=user_input_7,
                    credit_limit=user_input_8)
                a_class_instance.save()
                logging.info(f'a new record is Saved, \
                    new saved ID is {user_input_1} and name is {user_input_2}')
        except Exception as e:
            logging.info(e)
            logging.info(f'New record is Not saved, \
                ID is {user_input_1} and name is {user_input_2}')
    database.close()


def add_customer_csv(file_name):
    """
    This function write csv file into database
    generator is used to save memory
    """
    customer_list = create_customer_generator(file_name)
    _add_customers(customer_list)

def create_customer_generator(file_name):
    """
    this is a generator function to yield a row
    """
    fh = open("{}.csv".format(file_name))
    reader = csv.reader(fh)
    line = 0
    for row in reader:
        line += 1
        if line == 1:
            continue
        yield row
    fh.close()

def _search_customers(search_input=None):
    """
    This is a search customer function.
    Optional argumanet search_input is customer ID, format str.
    This function will return a dictionary object with name, lastname, email address
    and phone number of a customer or an empty dictionary object if no customer was found.
    return [
        [("998", "Name", "Lastname", "Address", "phone", "email", "active", 999),
         ("997", "Name", "Lastname", "Address", "phone", "email", "inactive", 10)],
        ("998", "000")
    ]
    """
    database = SqliteDatabase('customer.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    if search_input == None:
        search_input = input("What's the customer ID you want to search?")

    try:
        a_record = Customer.get(Customer.customer_id == search_input)
        a_dict = {a_record.customer_id: [
            a_record.name,
            a_record.last_name,
            a_record.home_address,
            a_record.phone_number,
            a_record.email_address,
            a_record.status,
            a_record.credit_limit]}
        logging.info(f'Searched item is found:{a_dict}')
        return a_dict

    except Exception as e:
        logging.info(f"{search_input} not found")
        logging.info(e)
        return {}



def _delete_customers(delete_input=None):
    """
    delete_customer(customer_id):
    This function will delete a customer from the sqlite3 database
    the customer_id is optional argument, format is str.
    """
    database = SqliteDatabase('customer.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    if delete_input == None:
        delete_input = input("Which ID would you like to delete?")
    try:
        with database.transaction():
            an_instance = Customer.get(Customer.customer_id == delete_input)
            an_instance.delete_instance()
            logging.info(f'{an_instance} is deleted')
    except Exception as e:
        logging.info(f'{delete_input} cannot be deleted')
        logging.info(e)
    database.close()

def _update_customer_credit(update_input=None, update_input_credit=None):
    """
    update_customer_credit(customer_id, credit_limit):
    This function will search an existing customer by customer_id and update their credit limit
    or raise a ValueError exception if the customer does not exist.
    """
    database = SqliteDatabase('customer.db')
    database.execute_sql('PRAGMA foreign_keys = ON;')
    if update_input == None:
        update_input = input("Which ID would you like to update?")
    if update_input_credit == None:
        update_input_credit = int(input("What's the new credit limit?"))
    try:
        with database.transaction():
            res = (Customer.update({Customer.credit_limit: Decimal(update_input_credit)})
                   .where(Customer.customer_id == update_input)
                   .execute())
            logging.info(f"ID:{update_input},\
            New credit:{Customer.select(Customer.credit_limit).where(Customer.customer_id == update_input)},\
            is saved")
    except Exception as e:
        logging.info(f"{update_input}, {update_input_credit}, is Not saved")
        logging.info(e)

def _list_active_customers():
    """
    list_active_customers():
    This function will return an integer with the number of customers
    whose status is currently active.
    """
    #query = Customer.select(Customer, Sale).join(Sale, JOIN.INNER).where(Sale.status == True)
    #for customer in query:
    #    print (customer.customer_name)
    #logging.info("print customers whose status is currently active")
    #number = query.count()
    query = Customer.select().where(Customer.status == True)
    for customer in query:
        print(customer.name)
    number = query.count()
    print(number)
    return number

#just put a random genertor example
def generator_num():
    n = 0
    while True:
        yield n
        n += 1

def display_customer_info():
    """
    display and view info from database
    """
    query = Customer.select()
    for customer in query:
        print(customer.name)
        print(customer)
        yield customer
