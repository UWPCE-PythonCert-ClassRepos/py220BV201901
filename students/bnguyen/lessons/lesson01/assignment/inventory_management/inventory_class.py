# Inventory class
"""
    Doctring is a must have for module/file.  This is a Inventory class.
"""


class Inventory():
    """
    Docstring is a must have for class.
    """
    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def __str__(self):
        return f"testing"

    def return_as_dictionary(self):
        """
        Method is also required a docstring.
        """
        output_dict = {}
        output_dict['productCode'] = self.product_code
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.market_price
        output_dict['rentalPrice'] = self.rental_price

        return output_dict
