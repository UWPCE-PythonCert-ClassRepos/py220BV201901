# Unit test
"""
This is the unit test module for the inventory management system
"""

from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.market_prices import get_latest_price


class InventoryTest(TestCase):

    def test_inventory(self):
        inv_dict_test = {'product_code': '555', 'description': 'black',
                         'market_price': 250, 'rental_price': 30}
        inv_dict = Inventory('555', 'black', 250, 30)
        self.assertEqual(inv_dict_test, inv_dict.return_as_dictionary())

class FurnitureTest(TestCase):

    def test_furniture(self):
        furn_dict_test = {'product_code': '555', 'description': 'black',
                         'market_price': 250, 'rental_price': 30,
                         'material': 'wood', 'size': 's'}
        furn_dict = Furniture('555', 'black', 250, 30, 'wood', 's')
        self.assertEqual(furn_dict_test, furn_dict.return_as_dictionary())

class ElectricApplianceTest(TestCase):

    def test_electric_appliances(self):
        elec_dict_test = {'product_code': '555', 'description': 'black',
                         'market_price': 250, 'rental_price': 30,
                         'brand': 'kirkland', 'voltage' :60}
        elec_dict = ElectricAppliances('555', 'black', 250, 30, 'kirkland', 60)
        self.assertEqual(elec_dict_test, elec_dict.return_as_dictionary())

class MarketPricesTest(TestCase):

    def test_market_prices(self):
        mkt_prc = 24
        self.assertEqual(mkt_prc, get_latest_price(mkt_prc))



class MainTestMock(TestCase):
    """
    Class for testing the main module in isolation from the projects classes using mocking
    """

    inv_dict_test = {'product_code': '555', 'description': 'black',
                     'market_price': 250, 'rental_price': 30}

    furn_dict_test = {'product_code': '555', 'description': 'black',
                      'market_price': 250, 'rental_price': 30,
                      'material': 'wood', 'size': 's'}

    elec_dict_test = {'product_code': '555', 'description': 'black',
                      'market_price': 250, 'rental_price': 30,
                      'brand': 'kirkland', 'voltage' :60}

    @patch('inventory_management.main.new_inventory_item', return_value=inv_dict_test)
    def test_new_inventory_item(self, new_inventory_item):
        inv_dict = {'product_code': '555', 'description': 'black',
                    'market_price': 250, 'rental_price': 30}
        self.assertEqual(new_inventory_item(), inv_dict)


    @patch('inventory_management.main.new_furniture_item', return_value=furn_dict_test)
    def test_new_furniture_item(self, new_furniture_item):
        furn_dict = {'product_code': '555', 'description': 'black',
                     'market_price': 250, 'rental_price': 30,
                     'material': 'wood', 'size': 's'}
        self.assertEqual(new_furniture_item(), furn_dict)


    @patch('inventory_management.main.new_electric_appliance_item', return_value=elec_dict_test)
    def test_new_electric_appliance_item(self, new_electric_appliance_item):
        elec_dict = {'product_code': '555', 'description': 'black',
                     'market_price': 250, 'rental_price': 30,
                     'brand': 'kirkland', 'voltage' :60}
        self.assertEqual(new_electric_appliance_item(), elec_dict)
