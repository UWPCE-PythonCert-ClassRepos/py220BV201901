# Inventory class
# pylint: disable=too-few-public-methods
"""
Module to define the inventory class
"""

class Inventory:
    """
    This is a class to add inventory attributes to a dictionary
    """

    def __init__(self, product_code, description, market_price, rental_price):
        """
        This is the constructor function to assign values to inventory attributes
        """
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price


    def return_as_dictionary(self):
        """
        Function to add the inventory attributes to a dictionary
        """
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict
