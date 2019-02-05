# Furniture class
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
"""
Module to define furniture class
"""

from inventory_management.inventory_class import Inventory

class Furniture(Inventory):
    """
    This class inherets from Inventory class and adds furniture attributes
    to a dictionary
    """

    def __init__(self, product_code, description, market_price, rental_price,
                 material, size):

        Inventory.__init__(self, product_code, description, market_price,
                           rental_price) # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """
        Function to add furniture attributes to a dictionary
        """
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
