# furniture_class
""" Create a subclass to get
an dict containing furniture items by getting basic info from inventory class"""
from inventory_management.inventory_class import Inventory

class Furniture(Inventory): # pylint: disable=too-few-public-methods
    """ Subclass of Inventory class to added more parameters"""

    # pylint: disable=too-many-arguments
    def __init__(self, product_code, description, market_price,
                 rental_price, material, size):
        Inventory.__init__(self, product_code, description,
                           market_price, rental_price)
        # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """ method to return a complete info of furniture items as dict"""
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
