"""
    Lesson05 tests
    HP Norton products in MongoDB

"""

import os
import unittest
import lesson07.assignment.hpnorton_products.parallel_database as mongo


class Testmongodatabase(unittest.TestCase):
    """ Tests for pymongo functions """

    def test_import_date(self):
        """ import data """

        directory = os.path.dirname(os.path.abspath(__file__))
        result = mongo.import_data(directory, 'products.csv', 'customers.csv', 'rentals.csv')

        assert result[0][0] == 9999
        assert result[1][0] == 9999
        assert result[2][0] == 9999


    def test_show_avail_products(self):
        """ test for available products """

        result = mongo.show_available_products()
        assert len(result) == 9999


    def test_show_rentals(self):
        """ test for available products """

        result = mongo.show_rentals("P000004")

        assert len(result) == 2
