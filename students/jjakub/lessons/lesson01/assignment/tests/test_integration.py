# Integration test
"""
This is the integration test module for the inventory management system
"""

from unittest import TestCase
from inventory_management.main import add_new_item
from inventory_management.main import new_inventory_item
from inventory_management.main import new_furniture_item
from inventory_management.main import new_electric_appliance_item
from inventory_management.main import get_market_price

class MainTest(TestCase):
    """
    Class for testing the main modules integration with the projects classes
    """

    def test_new_inventory_item(self):
        inv_dict_test = {'product_code': '555', 'description': 'black',
                         'market_price': 250, 'rental_price': 30}
        inv_dict = new_inventory_item('555', 'black', 250, 30)
        self.assertEqual(inv_dict_test, inv_dict.return_as_dictionary())


    def test_new_furniture_item(self):
        furn_dict_test = {'product_code': '555', 'description': 'black',
                          'market_price': 250, 'rental_price': 30,
                          'material': 'wood', 'size': 's'}
        furn_dict = new_furniture_item('555', 'black', 250, 30, 'wood', 's')
        self.assertEqual(furn_dict_test, furn_dict.return_as_dictionary())


    def test_new_electric_appliance_item(self):
        elec_dict_test = {'product_code': '555', 'description': 'black',
                          'market_price': 250, 'rental_price': 30,
                          'brand': 'kirkland', 'voltage' :60}
        elec_dict = new_electric_appliance_item('555', 'black', 250, 30, 'kirkland', 60)
        self.assertEqual(elec_dict_test, elec_dict.return_as_dictionary())


    def test_get_market_price(self):
        mkt_prc = 24
        self.assertEqual(mkt_prc, get_market_price(mkt_prc))
