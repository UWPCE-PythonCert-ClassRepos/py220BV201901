'''
Unit testing for the various functions in basic_operations module
'''

# Import basic_operations module for functions to be tested.
from basic_operations import *

# Create the database 'customers.db'.  Subsequent attempts to run script do
# not disturb 'customers.db' database if it already exists--as expected.
create_database()

# Some test customer records to add to the database.
cust_list = [
    (1111, 'Dave', 'Arasim', '11 Cherry Lane', 2065551111,
     'dave@hotmail.com', True, 1000),
    (2222, 'Daniel', 'Ash', '22 Apple Ave', 4255552222,
     'daniel@yahoo.com', True, 2000),
    (3333, 'Steve', 'Howe', '33 Orange Blvd', 4255553333,
     'steve@gmail.com', True, 3000),
    (4444, 'Tony', 'Levin', '44 Banana Ct', 4255554444,
     'tony@hotmail.com', True, 4000),
    (5555, 'Randy', 'Rhoads', '55 Lime Way', 4255555555,
     'randy@yahoo.com', True, 5000),
    ]

# Adding test customers from 'cust_list' above.
for this_cust in cust_list:
    add_customer(this_cust)

# Print out all the customers records to show they were successfully added.
show_customers()

# Search for customers in database and return as dictionary object.
# Note: cust_id '2222' is expected to be there, but cust_id '9999' is not.
cust_ids = [2222, 9999]
for this_cust_id in cust_ids:
    search_customer(this_cust_id)

# Delete customers from database.
# Note: cust_id '2222' is expected to be there, but cust_id '9999' is not.
cust_ids = [2222, 9999]
for this_cust_id in cust_ids:
    delete_customer(this_cust_id)

# Print out all the customers records to show '2222' was successfully deleted.
show_customers()

# Update customer records in database for 'status'.
# Note: cust_id '3333' is expected to be there, but cust_id '9999' is not.
update_customer(3333, 'status', False) # Existing customer status
update_customer(9999, 'status', False) # Non-existing customer status

# Update customer records in database for 'cred_limit'.
# Note: cust_id '3333' is expected to be there, but cust_id '9999' is not.
update_customer(3333, 'cred_limit', 6000) # Existing customer credit
update_customer(9999, 'cred_limit', 9000) # Non-existing customer credit

# Return count of active customers as integer ('status' == True)
list_customers()

# Print out all the customers records to show successful content/updates.
show_customers()
