'''
Unit testing for the various classes in inventory_management modules
'''

# Import testing modules
from unittest import TestCase

# Import Inventory Management modules
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
import inventory_management.market_prices as market_prices
#import inventory_management.main as main  DKA:  I can't get this to load (when uncommented) when I invoke with unittest and therefore cannot work on 'class MainTest()' below

full_inventory = {}  # Store all inventory items

# Inventory attributes
item_code = 1
item_description = 'Guitar'
item_price = 1000.00
item_rental_price = 50.00

# Electric Appliance attributes
elec_code = 2
elec_description = 'Washer'
elec_price = 1500.00
elec_rental_price = 75.00
elec_brand = 'Whirlpool'
elec_voltage = 110

# Furniture attributes
furn_code = 3
furn_description = 'Table'
furn_price = 500.00
furn_rental_price = 25.00
furn_material = 'Wood'
furn_size = 'Medium'

# Market Price (hard-coded value: 24)
market_price = 24

##############################################################################

class InventoryTest(TestCase):
    '''Test inventory_class.py module'''

    def test_inventory(self):
        inventory = Inventory(item_code, item_description,
                              item_price, item_rental_price)
        
        full_inventory[item_code] = inventory.return_as_dictionary()

        self.assertTrue(item_code in full_inventory)

        this_item = full_inventory[item_code]

        self.assertTrue(this_item['product_code'] == item_code)
        self.assertTrue(this_item['description'] == item_description)
        self.assertTrue(this_item['market_price'] == item_price)
        self.assertTrue(this_item['rental_price'] == item_rental_price)


class ElectricAppliancesTest(TestCase):
    '''Test electric_appliances_class.py module'''

    def test_electric_appliances(self):
        elec_app = ElectricAppliances(elec_code, elec_description, elec_price,
                                      elec_rental_price, elec_brand, elec_voltage)
        
        full_inventory[elec_code] = elec_app.return_as_dictionary()

        self.assertTrue(elec_code in full_inventory)

        this_item = full_inventory[elec_code]

        self.assertTrue(this_item['product_code'] == elec_code)
        self.assertTrue(this_item['description'] == elec_description)
        self.assertTrue(this_item['market_price'] == elec_price)
        self.assertTrue(this_item['rental_price'] == elec_rental_price)
        self.assertTrue(this_item['brand'] == elec_brand)
        self.assertTrue(this_item['voltage'] == elec_voltage)


class FurnitureTest(TestCase):
    '''Test furniture_class.py module'''

    def test_furniture(self):
        furniture = Furniture(furn_code, furn_description, furn_price,
                              furn_rental_price, furn_material, furn_size)
        
        full_inventory[furn_code] = furniture.return_as_dictionary()

        self.assertTrue(furn_code in full_inventory)

        this_item = full_inventory[furn_code]

        self.assertTrue(this_item['product_code'] == furn_code)
        self.assertTrue(this_item['description'] == furn_description)
        self.assertTrue(this_item['market_price'] == furn_price)
        self.assertTrue(this_item['rental_price'] == furn_rental_price)
        self.assertTrue(this_item['material'] == furn_material)
        self.assertTrue(this_item['size'] == furn_size)


class MarketPricesTest(TestCase):
    '''Test market_prices.py module'''

    def test_market_prices(self):
        self.assertTrue(market_prices.get_latest_price(item_code) == market_price)


class MainTest(TestCase):
    '''Test main.py module'''
    pass  #DKA:  I cannot get started on this because the 'import inventory_management.main as main' above does not work