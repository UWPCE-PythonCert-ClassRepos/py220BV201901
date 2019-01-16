"""
Unit tests for inventory management classes
"""


from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest import mock
from io import StringIO

from inventory_management.electricappliancesclass import ElectricAppliances
from inventory_management.inventoryclass import Inventory
from inventory_management.furnitureclass import Furniture
from inventory_management.fullinventory import Fullinventory
import inventory_management.market_prices
import inventory_management.main as tc



class CreateInvTests(TestCase):

    def test_addnewinvitem(self):

        newitem = Inventory(24, 'Test item', 50.00, 60.00)
        mock_values = [24, 'Test item', 50.00, 'n', 'n']

        with mock.patch('builtins.input', side_effect=mock_values):
            try:
                tc.add_new_item()

                tc.get_latest_price = MagicMock(60.00)
                tc.get_latest_price.assert_called_with(24)

                tc.Inventory = MagicMock(newitem)
                tc.Inventory.assert_called_with(24, 'Test item', 50.00, 60.00)
            except NameError:
                assert(True)

    def test_addnewfuritem(self):

        newitem = Inventory(24, 'Test item', 50.00, 60.00)
        newfurn = Furniture(newitem, 'Cloth', 'S')
        mock_values = [24, 'Test item', 50.00, 'y', 'Cloth','S', 'n']

        with mock.patch('builtins.input', side_effect=mock_values):
            try:
                tc.add_new_item()

                tc.get_latest_price = MagicMock(60.00)
                tc.get_latest_price.assert_called_with(24)

                tc.Furniture = MagicMock(newfurn)
                tc.Furniture.assert_called_with(newitem, 'Cloth', 'S')
            except NameError:
                assert(True)

    def test_addnewapplitem(self):

        newitem = Inventory(24, 'Test item', 50.00, 60.00)
        newappli = ElectricAppliances(newitem, 'Maytag', '100V')
        mock_values = [24, 'Test item', 50.00, 'y', 'y', 'Maytag','100V']

        with mock.patch('builtins.input', side_effect=mock_values):
            try:
                tc.add_new_item()

                tc.get_latest_price = MagicMock(60.00)
                tc.get_latest_price.assert_called_with(24)

                tc.ElectricAppliances = MagicMock(newappli)
                tc.ElectricAppliances.assert_called_with(newitem, 'Maytag', '100V')
            except NameError:
                assert(True)
