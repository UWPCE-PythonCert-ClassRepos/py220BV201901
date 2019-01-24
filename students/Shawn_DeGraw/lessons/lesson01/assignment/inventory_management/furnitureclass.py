"""
Furniture Class module
"""


class Furniture():
    """ Furniture class returns dictionary of furniture. """

    def __init__(self, inv_item, material, size):

        self.inv_item = inv_item
        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """ Method to create furniture dictionary. """

        output_dict = self.inv_item.return_as_dictionary()
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
