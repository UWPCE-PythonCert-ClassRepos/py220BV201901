"""
This module provides a subtraction operator.
"""
class Subtracter(object):
    """
    Substracting class.
    """
    @staticmethod
    def calc(operand_1, operand_2):
        """
        Seems like docstring is more line than code
        """
        return operand_1 - operand_2  #ORG:This yield negative values in integration test
        #return operand_2 - operand_1  #This call unit test to fail
