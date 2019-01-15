# Inventory class
'''
Inventory module
'''
class Inventory:
    '''
    Inventory
    '''
    def __init__(self, product_code, description, market_price, rental_price):
        self.__product_code = product_code
        self.__description = description
        self.__market_price = market_price
        self.__rental_price = rental_price

    @property
    def product_code(self):
        '''
        Return property of product_code
        '''
        return self.__product_code

    @property
    def description(self):
        '''
        Return property of description
        '''
        return self.__description

    @property
    def market_price(self):
        '''
        Return property of market_price
        '''
        return self.__market_price

    @property
    def rental_price(self):
        '''
        Return property of rental_price
        '''
        return self.__rental_price

    def return_as_dictionary(self):
        '''
        Return Inventory as a dictionary
        '''
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict
