# Furniture class
"""
What does this do?
"""
#from inventory_management.inventory_class import Inventory
from inventory_class import Inventory


class Furniture(Inventory):
    """
    What does this do?
    """
    def __init__(self, product_code, description, market_price, rental_price, material, size):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        #super().__init__(self, product_code, description, market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        out_put_dict = {}
        out_put_dict['product_code'] = self.product_code
        out_put_dict['description'] = self.description
        out_put_dict['market_price'] = self.market_price
        out_put_dict['rental_price'] = self.rental_price
        out_put_dict['material'] = self.material
        out_put_dict['size'] = self.size

        return out_put_dict
