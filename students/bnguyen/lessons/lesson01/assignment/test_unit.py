#Student: Bradnon Nguyen
#Class:   Advance Python 220 - Jan2019
#Lesson01 - test_unit module
"""
What does this do?
To test all the methods in inv module
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management import inventory_class
from inventory_management.market_prices import get_latest_price
#from inventory_management.main import main_menu
import inventory_management.main as m


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

        expect_values = {'1':m.add_new_item, '2':m.item_info,
                         'q':m.exit_program}
        user_inputs = ['1', '2', 'q']

        for i in range(3):
            with patch('builtins.input', return_value=user_inputs[i]):
                result = m.main_menu()
                self.assertEqual(result, expect_values.get(user_inputs[i]))

#More main testing needed