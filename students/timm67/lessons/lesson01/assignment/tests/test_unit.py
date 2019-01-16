""" Unit tests for assignment01 """
from unittest import TestCase
from unittest.mock import MagicMock

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.market_prices import get_latest_price


class InventoryTest(TestCase):
    """ Inventory class tests """
    def test_inventory_class(self):
        """ Inventory class test """
        product_code = 1234
        description = 'test inventory article'
        market_price = 1234.56
        rental_price = 12.34

        test_article = Inventory(product_code, description, market_price, rental_price)
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

        test_article = Furniture(product_code, description, market_price, rental_price,
                                 material, size)
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
        mock = MagicMock(return_value=magic_num)
        item_code = 42
        mkt_price = mock(item_code)
        mock.assert_called_with(item_code)
        self.assertEqual(mkt_price, magic_num)


class CliTest(TestCase):
    """cli (main) test"""
    def test__call(self):
        """ foo """
        pass
        # self.subtracter.calc = MagicMock(return_value=(2-1))
        # self.subtracter.calc.assert_called_with(2, 1)
        # self.assertEqual(result, (2-1))
