""" Unit tests for assignment01 """
from unittest import TestCase

from basic_operations import add_customer
from basic_operations import search_customer
from basic_operations import delete_customer
from basic_operations import update_customer_credit
from basic_operations import list_active_customers

from loguru import logger
from sys import stdout

logger.add(stdout, level='INFO')
logger.enable(__name__)

class MainTest(TestCase):
    """Main test"""
    def test_add_furniture(self):
        """ Test adding a furniture item """
        pass