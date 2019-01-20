"""
Module:calculator with basic methods.
"""
from .exceptions import InsufficientOperands

#class Calculator(object):
class Calculator:
    """
    Class: Calculator
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        Method: To enter number.
        """
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """
        Method: To do calculation.
        """
        try:
            #result = operator.calc(self.stack[0], self.stack[1]) #ORG
            result = operator.calc(self.stack[1], self.stack[0])  #Integration test to pass
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """
        Method: To add 2 number.
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        Method: To substract 2 numbers.
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        Method: To substract 2 numbers.
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        Method: To divide 2 numbers.
        """
        return self._do_calc(self.divider)
