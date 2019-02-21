from lesson03.assignment.management_database_model import *

import logging

logging.basicConfig(level=logging.INFO)

logging.info('One off program to build the classes from the model in the database')

database.create_tables([
        Customer,
        Sale,
    ])

database.close()