"""hw3, sqlite databass, Peewee"""

from lesson03.assignment.management_database_model import *
import logging

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

def add_customer():
    """
    add a new customer record to database Customer table
    (customer_id, name, lastname, home_address, phone_number, email_address, status, credit_limit)
    """
    logging.info("connect to data base")
    database = SqliteDatabase('customer.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    logging.info("getting user input")
    user_input_1 = input("What's the ID you would like for the new customer?")
    user_input_2 = input("What's the customer's name?")
    user_input_3 = input("What's the last name?")
    user_input_4 = input("What's the home address?")
    user_input_5 = input("phone number")
    user_input_6 = input("email")
    user_input_7 = input("What's the allowed credit limit?")
    try:
        with database.transaction():
            a_class_instance = Customer.create(customer_id=user_input_1,
                                customer_name=user_input_2,
                                last_name=user_input_3,
                                home_address=user_input_4,
                                phone_number=user_input_5,
                                email=user_input_6,
                                credit_limit=user_input_7)
            a_class_instance.save()
            logging.info(f'a new record is Saved, new saved ID is {user_input_1} and name is {user_input_2}')
    except Exception as e:
        logging.info(e)
        logging.info(f'New record is Not saved, ID is {user_input_1} and name is {user_input_2}')

    database.close()

def add_customers(a_dict):
    """
    attribute is a dict of new customers, dict key is customer ID,
    Value is a list of customer informations as needed by table Customer.
    This function add the dict to the database.
    """
    database = SqliteDatabase('customer.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    try:
        with database.transaction():
            for key, value in a_dict.items():
                new_record = Customer.create(customer_id=key,
                                    customer_name=value[0],
                                    last_name=value[1],
                                    home_address=value[2],
                                    phone_number=value[3],
                                    email=value[4],
                                    credit_limit=value[5])
                new_record.save()
                logging.info(f"A new record in the list is saved to database, ID is {key}")
        logging.info("a dictionary of data is saved")

    except Exception as e:
        logging.info(e)
        logging.info(f'Recored ID:{key} is not saved')

    database.close()

def search_customer(search_input=None):
    """
    This is a search customer function.
    Optional argumanet search_input is customer ID, format str.
    This function will return a dictionary object with name, lastname, email address 
    and phone number of a customer or an empty dictionary object if no customer was found.
    """
    database = SqliteDatabase('customer.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    if search_input == None:
        search_input = input("What's the customer ID you want to search?")

    try:
        a_record = Customer.get(Customer.customer_id == search_input)
        a_dict = {a_record.customer_id: [a_record.customer_name,
                                        a_record.last_name,
                                        a_record.email,
                                        a_record.phone_number]}
        logging.info(f'Searched item is found:{a_dict}')
        return a_dict

    except Exception as e:
        logging.info(f"{search_input} not found")
        logging.info(e)
        return {}

    database.close()


def delete_customer(delete_input=None):
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

def update_customer_credit(update_input=None, update_input_credit=None):
    """
    update_customer_credit(customer_id, credit_limit):
    This function will search an existing customer by customer_id and update their credit limit
    or raise a ValueError exception if the customer does not exist.
    """
    database = SqliteDatabase('customer.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    if update_input == None:
        update_input = input("Which ID would you like to update?")
    if update_customer_credit == None:
        update_input_credit = int(input("What's the new credit limit?"))
    try:
        with database.transaction():
            a_record = Customer.get(Customer.customer_id == update_input)
            a_record.credit_limit = update_customer_credit
            a_record.save()
            #print(a_record.credit_limit)
            logging.info(f"ID:{update_input}, New credit:{a_record.credit_limit}, is saved")
    except Exception as e:
        logging.info(f"{update_input}, {update_input_credit}, is Not saved")
        logging.info(e)

    database.close()

def add_sales(new_sales_dict):
    """
    add a dict of new sale records to database Sale table
    order_number is key,
    value is a list, which includes following informatio
    order_date = DateField(formats='YYYY-MM-DD')
    status = BooleanField(help_text='True means active, False means in-active', null=False)
    customer_id = ForeignKeyField(Customer, related_name='was filled by', null=False)
    """
    logging.info("connect to data base")
    database = SqliteDatabase('customer.db')
    database.connect()
    database.create_tables([Customer, Sale])
    database.execute_sql('PRAGMA foreign_keys = ON;')

    for key, value in new_sales_dict.items():
        #try:
        with database.transaction():
            a_class_instance = Sale.create(order_number=key,
                                    order_date=value[0],
                                    status=value[1],
                                    customer_id=value[2])
            a_class_instance.save()
            logging.info(f'a new record is Saved, new saved order number is {key} and customer status is {value[1]}')
        """except Exception as e:
            logging.info(e)
            logging.info(f'New record is Not saved, order number is {key} and status is {key[1]}')
"""
    #logging.info("Dict is saved")
    database.close()

def list_active_customer():
    """
    list_active_customers():
    This function will return an integer with the number of customers whose status is currently active.
    """
    query = Customer.select(Customer, Sale).join(Sale, JOIN.INNER).where(Sale.status == True)
    for customer in query:
        print (customer.customer_name)
    logging.info("print customers whose status is currently active")
    number = query.count()
    logging.info(f'the number of customers whose status is currently active is {number}')
    database.close()
    return number
