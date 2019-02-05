from basic_operations import add_customer
from basic_operations import search_customer
from basic_operations import delete_customer
from basic_operations import update_customer_credit
from basic_operations import list_active_customers

from loguru import logger
from sys import stdout

from peewee import *


#database = SqliteDatabase('personjob.db')
#database.connect()
#database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only


def main():
    """
    Ensure you application will create an empty database if one doesn’t exist
    when the app is first run. Call it customers.db
    """

    # Standalone function to initialize logging

    logger.add(sys.stdout, level='INFO')
    logger.add("logfile_{time}.txt", level='DEBUG')
    logger.enable(__name__)


if  __name__ == '__main__':
    main()
