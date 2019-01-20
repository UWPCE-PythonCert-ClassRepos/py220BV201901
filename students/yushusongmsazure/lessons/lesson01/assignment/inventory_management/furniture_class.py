# Furniture class
'''
Furniture module
'''
from inventory_class import Inventory

class Furniture(Inventory):
    '''
    Furniture class
    '''

    def __init__(self, **kwargs):
        self.__material = kwargs.pop('material')
        self.__size = kwargs.pop('size')
        super().__init__(**kwargs)

    @property
    def material(self):
        '''
        Return property of material
        '''
        return self.__material

    @property
    def size(self):
        '''
        Return property of size
        '''
        return self.__size

    def return_as_dictionary(self):
        '''
        Return Inventory as a dictionary
        '''
        return {
            **super().return_as_dictionary(),
            'size': self.size,
            'material': self.material
        }
