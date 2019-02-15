'''
Unit testing for the various functions in basic_operations module
'''

# Import basic_operations module for functions to be tested.
from basic_operations import *

# Create the database 'customers.db'.  Subsequent attempts to run script do
# not disturb 'customers.db' database if it already exists--as expected.
drop_database()
