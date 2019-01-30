# Student: Bradnon Nguyen
# Class:   Advance Python 220 - Jan2019
# Lesson01 - test_unit module
"""
What does this do?
To test all the methods in inv module
"""

import sys
from io import StringIO
from unittest import TestCase
from unittest.mock import patch, MagicMock

# Testing out Andy EXPORT PYTHONPATH=. worked!  VSCode still complaint[E0401].
import inventory_management.main as m
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management import inventory_class
from inventory_management.market_prices import get_latest_price


class InventoryTests(TestCase):
    """
    What does this do?
    """
    def setUp(self):
        self.product_code = 24
        self.description = "Junk"
        self.market_price = get_latest_price(self.product_code)
        self.rental_price = 30

        self.inventory = inventory_class.Inventory(
            self.product_code, self.description,
            self.market_price, self.rental_price)

    def test_return_as_dictionary_call(self):
        """
        This method tests Inventory.return_as_dictionary().
        """

        dict_result = self.inventory.return_as_dictionary()

        expected_dict = {}
        expected_dict['productCode'] = 24
        expected_dict['description'] = "Junk"
        expected_dict['marketPrice'] = 24
        expected_dict['rentalPrice'] = 30

        self.assertEqual(expected_dict, dict_result)


class ElectricAppliancesTests(TestCase):
    """
    To test ElectricAppliances class and method.
    """
    def setUp(self):
        self.product_code = 22
        self.description = "Lamb"
        self.market_price = get_latest_price(self.product_code)
        self.rental_price = 22
        self.brand = "GE"
        self.voltage = "210"

        self.electrical = ElectricAppliances(
            self.product_code, self.description,
            self.market_price, self.rental_price,
            self.brand, self.voltage)

    def test_return_as_dictionary_call3(self):
        """
        This
        """
        dict_result = self.electrical.return_as_dictionary()

        expected_dict = {}
        expected_dict['product_code'] = 22
        expected_dict['description'] = "Lamb"
        expected_dict['market_price'] = 24
        expected_dict['rental_price'] = 22
        expected_dict['brand'] = "GE"
        expected_dict['voltage'] = "210"

        self.assertEqual(expected_dict, dict_result)


class FurnitureTests(TestCase):
    """
    To test Furniture class and method.
    """
    def setUp(self):
        self.product_code = 23
        self.description = "Table"
        self.market_price = get_latest_price(self.product_code)
        self.rental_price = 23
        self.material = "Wood"
        self.size = "L"

        self.furniture = Furniture(
            self.product_code, self.description,
            self.market_price, self.rental_price,
            self.material, self.size)

    def test_return_as_dictionary_call2(self):
        """
        This
        """
        dict_result = self.furniture.return_as_dictionary()

        expected_dict = {}
        expected_dict['product_code'] = 23
        expected_dict['description'] = "Table"
        expected_dict['market_price'] = 24
        expected_dict['rental_price'] = 23
        expected_dict['material'] = "Wood"
        expected_dict['size'] = "L"

        self.assertEqual(expected_dict, dict_result)


class MainTest(TestCase):
    """This class is used to test all the codes in main module"""

    def test_main_menu(self):
        """Test main menu to see if it return correctly"""

        expect_values = {'1': m.add_new_item, '2': m.item_info,
                         'q': m.exit_program}
        user_inputs = ['1', '2', 'q']

        for i in range(3):
            with patch('builtins.input', return_value=user_inputs[i]):
                result = m.main_menu()
                self.assertEqual(result, expect_values.get(user_inputs[i]))

    def test_add_new_item(self):
        """
        This is to test the method add_new_item() in main module.
        There is multipe path for this method.  Therefore we must cover
        all 3 path: inventory, furniture, and electric.
        """
        # Test path 1: mock insert base inventory and compare
        expected_dict = {1234: {'productCode': 1234,
                                'description': 'This is a base item.',
                                'marketPrice': 30, 'rentalPrice': 25},
                         1235: {'product_code': 1235,
                                'description': 'Furniture item.',
                                'market_price': 33, 'rental_price': 26,
                                'material': 'Wood', 'size': 'M'},
                         1236: {'product_code': 1236,
                                'description': 'Electric item.',
                                'market_price': 33, 'rental_price': 27,
                                'brand': 'GE', 'voltage': 110}, }
        mock_values_1 = [1234, "This is a base item.", '25', "n", "n"]
        with patch('builtins.input', side_effect=mock_values_1):
            m.get_latest_price = MagicMock(return_value=30)  # Spec meet.
            m.add_new_item()

        # Test path 2: mock insert with furniture
        mock_values_2 = [1235, "Furniture item.", '26', "y", "Wood", "M"]
        with patch('builtins.input', side_effect=mock_values_2):
            m.get_latest_price = MagicMock(return_value=33)  # Spec meet.
            m.add_new_item()

        # Test path 3: mock insert with electric without mock price
        mock_values_3 = [1236, "Electric item.", '27', "n", "y", "GE", 110]
        with patch('builtins.input', side_effect=mock_values_3):
            m.get_latest_price(1236)  # shame that the value 33 stuck
            m.add_new_item()

        self.assertEqual(m.FULL_INVENTORY, expected_dict)

    def test_item_info(self):
        """This is to test the method item_info() in main module."""
        expected_dict = {12344: {'productCode': 12344,
                                 'description': 'This is a base item.',
                                 'marketPrice': 24, 'rentalPrice': 25},
                         12355: {'product_code': 1235,
                                 'description': 'This is a furniture item.',
                                 'market_price': 25, 'rental_price': 26,
                                 'material': 'Wood', 'size': 'M'}, }
        m.FULL_INVENTORY = expected_dict
        # Testing else path
        with patch('builtins.input', return_value=12345):
            temp_stdout = StringIO()
            sys.stdout = temp_stdout
            m.item_info()
            output = temp_stdout.getvalue().strip()
            assert output == 'Item not found in inventory'

        # Testing the main path with correct iteim id
        # Item id can be replaced to test more or build a loop
        with patch('builtins.input', return_value=12344):
            str_expect = ("productCode:12344\n"
                          "description:This is a base item.\n"
                          "marketPrice:24\n"
                          "rentalPrice:25")
            temp_stdout = StringIO()
            sys.stdout = temp_stdout
            m.item_info()
            output = temp_stdout.getvalue().strip()
            self.assertEqual(str_expect, output)

    def test_exit_program(self):
        """To test the exit_program method in main"""
        with self.assertRaises(SystemExit) as exit_code:
            m.exit_program()
            self.assertEqual(exit_code.exception.code, 1)

    def test_get_price(self):
        """To test the get_price method in main, for coverage."""
        str_txt = "Get price 1234"
        temp_stdout = StringIO()
        sys.stdout = temp_stdout
        m.get_price(1234)
        output = temp_stdout.getvalue().strip()
        self.assertEqual(str_txt, output)
