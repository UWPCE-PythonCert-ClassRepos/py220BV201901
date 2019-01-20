# Electric appliances class
'''
Appliances class
'''
from inventory_class import Inventory

class ElectricAppliances(Inventory):
    '''
    Electric Appliances
    '''
    def __init__(self, **kwargs):
        self.__brand = kwargs.pop('brand')
        self.__voltage = kwargs.pop('voltage')
        super().__init__(**kwargs)

    @property
    def brand(self):
        '''
        Return property of brand
        '''
        return self.__brand

    @property
    def voltage(self):
        '''
        Return property of voltage
        '''
        return self.__voltage

    def return_as_dictionary(self):
        '''
        Return Inventory as a dictionary
        '''
        return {
            **super().return_as_dictionary(),
            'brand': self.brand,
            'voltage': self.voltage
            }
