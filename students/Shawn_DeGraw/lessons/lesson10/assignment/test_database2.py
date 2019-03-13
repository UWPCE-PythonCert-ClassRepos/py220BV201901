"""
    Lesson10 tests
    HP Norton products in MongoDB

"""

import os
import unittest
import lesson10.assignment.hpnorton_products.database as mongo


class Testmongodatabase(unittest.TestCase):
    """ Tests for pymongo functions """

    def test_import_date(self):
        """ import data """

        directory = os.path.dirname(os.path.abspath(__file__))
        # mongo.import_data = mongo.decorator(mongo.import_data)
        resultgood, resultfail = mongo.import_data(directory, 'products.csv', 'customers.csv', 'rentals.csv')

        assert resultgood == (9999, 9999, 9999)
        assert resultfail == (0, 0, 0)


    def test_show_avail_products(self):
        """ test for available products """

        # mongo.show_available_products = mongo.decorator(mongo.show_available_products)
        result = mongo.show_available_products()
        assert len(result) == 9999


    def test_show_rentals(self):
        """ test for available products """

        # mongo.show_rentals = mongo.decorator(mongo.show_rentals)
        result = mongo.show_rentals("P000004")

        assert len(result) == 2
