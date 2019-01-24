""" Unit tests for assignment01 """
from unittest import TestCase
# from unittest.mock import MagicMock

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.market_prices import get_latest_price
from inventory_management.main import add_appliance
from inventory_management.main import add_furniture
from inventory_management.main import add_inventory
from inventory_management.main import get_item

class InventoryTest(TestCase):
    """ Inventory class tests """
    def test_inventory_class(self):
        """ Inventory class test """
        product_code = 1234
        description = 'test inventory article'
        market_price = 1234.56
        rental_price = 12.34

        test_article = Inventory(product_code, description, market_price,
                                 rental_price)
        test_dict = test_article.return_as_dictionary()

        self.assertEqual(test_dict['product_code'], product_code)
        self.assertEqual(test_dict['description'], description)
        self.assertEqual(test_dict['market_price'], market_price)
        self.assertEqual(test_dict['rental_price'], rental_price)


class FurnitureTest(TestCase):
    """ Furniture class tests """
    def test_furniture_class(self):
        """ Furniture class test """
        product_code = 5678
        description = 'test furniture article'
        market_price = 5678.90
        rental_price = 56.78
        material = 'cloth'
        size = 'large'

        test_article = Furniture(product_code, description, market_price,
                                 rental_price, material, size)
        test_dict = test_article.return_as_dictionary()

        self.assertEqual(test_dict['product_code'], product_code)
        self.assertEqual(test_dict['description'], description)
        self.assertEqual(test_dict['market_price'], market_price)
        self.assertEqual(test_dict['rental_price'], rental_price)
        self.assertEqual(test_dict['material'], material)
        self.assertEqual(test_dict['size'], size)


class ElectricApplianceTest(TestCase):
    """ Appliance class tests """
    def test_electric_appliance_class(self):
        """ Appliance class test """
        product_code = 5678
        description = 'test furniture article'
        market_price = 5678.90
        rental_price = 56.78
        brand = 'General Electric'
        voltage = 220

        test_article = ElectricAppliances(product_code, description,
                                          market_price, rental_price,
                                          brand, voltage)
        test_dict = test_article.return_as_dictionary()

        self.assertEqual(test_dict['product_code'], product_code)
        self.assertEqual(test_dict['description'], description)
        self.assertEqual(test_dict['market_price'], market_price)
        self.assertEqual(test_dict['rental_price'], rental_price)
        self.assertEqual(test_dict['brand'], brand)
        self.assertEqual(test_dict['voltage'], voltage)


class MarketPriceTest(TestCase):
    """market price test"""
    def test_market_price(self):
        """market price test"""
        magic_num = 24
        item_code = 42
        mkt_price = get_latest_price(item_code)
        self.assertEqual(mkt_price, magic_num)


class MainTest(TestCase):
    """Main test"""
    def test_add_furniture(self):
        """ Test adding a furniture item """
        item_code = 123
        item_description = 'sofa'
        item_price = 42
        item_rental_price = 24
        item_material = 'cloth'
        item_size = 'large'
        actual_dict = None
        test_dict = {
            'product_code' : item_code,
            'description' : item_description,
            'market_price' : item_price,
            'rental_price' : item_rental_price,
            'material' : item_material,
            'size' : item_size
        }

        add_furniture(item_code, item_description, item_price,
                      item_rental_price, item_material, item_size)

        actual_dict = get_item(item_code)

        self.assertNotEqual(actual_dict, None)
        if actual_dict is None:
            return

        for key in actual_dict:
            self.assertEqual(test_dict[key], actual_dict[key])


    def test_add_appliance(self):
        """ test adding an Electric Appliance item """
        item_code = 456
        item_description = 'dishwasher'
        item_price = 420
        item_rental_price = 240
        item_brand = 'GE'
        item_voltage = 220
        actual_dict = None

        test_dict = {
            'product_code' : item_code,
            'description' : item_description,
            'market_price' : item_price,
            'rental_price' : item_rental_price,
            'brand' : item_brand,
            'voltage' : item_voltage
        }

        add_appliance(item_code, item_description, item_price,
                      item_rental_price, item_brand, item_voltage)

        actual_dict = get_item(item_code)

        self.assertNotEqual(actual_dict, None)
        if actual_dict is None:
            return

        for key in actual_dict:
            self.assertEqual(test_dict[key], actual_dict[key])


    def test_add_inventory(self):
        """ Test adding an inventory item """
        item_code = 789
        item_description = 'pencil'
        item_price = 4
        item_rental_price = 2
        actual_dict = None

        test_dict = {
            'product_code' : item_code,
            'description' : item_description,
            'market_price' : item_price,
            'rental_price' : item_rental_price,
        }

        add_inventory(item_code, item_description, item_price,
                      item_rental_price)

        actual_dict = get_item(item_code)

        self.assertNotEqual(actual_dict, None)
        if actual_dict is None:
            return

        for key in actual_dict:
            self.assertEqual(test_dict[key], actual_dict[key])
