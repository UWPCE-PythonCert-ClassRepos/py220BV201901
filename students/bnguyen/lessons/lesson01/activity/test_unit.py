"""
What does this do?
To test all the methods in calculator module
"""
from unittest import TestCase
from unittest.mock import MagicMock

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands

class AdderTests(TestCase):
    """
    What does this do?
    """
    def test_adding(self):
        """
        What does this do?
        """
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))


class SubtracterTests(TestCase):
    """
    What does this do?
    """
    def test_subtracting(self):
        """
        What does this do?
        """
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))

        # self.assertEqual(-2 - -1, subtracter.calc(-2, -1))

#MultiplierTests and DividerTests as the requirement
class MultiplierTests(TestCase):
    """
    This is to test the Multiplier class
    """

    def test_multiplier(self):
        """
        This is to test the Multiplier class
        """
        multiplier = Multiplier()
        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i * j, multiplier.calc(i, j))

class DividerTests(TestCase):
    """
    This is to test the Multiplier class
    """
    def test_divider(self):
        """
        This is to test the Multiplier class
        """
        divider = Divider()
        for i in range(-10, 10):
            for j in range(-20, 20, 3): #skip 0 cheat!ZeroDivisionError:
                self.assertEqual(i/j, divider.calc(i, j))
        #self.assertEqual(1 / -1, divider.calc(1, -1))


class CalculatorTests(TestCase):
    """
    What does this do?
    """
    def setUp(self):
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(self.adder, self.subtracter, self.multiplier, self.divider)

    def test_insufficient_operands(self):
        """
        What does this do?
        """
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder_call(self):
        """
        What does this do?
        """
        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(1, 2)


    def test_subtracter_call(self):
        """
        What does this do?
        """
        self.subtracter.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()

        self.subtracter.calc.assert_called_with(1, 2)

    def test_multiplier_call(self):
        """
        This is to test calcultor.multipy method call.
        """
        self.multiplier.calc = MagicMock(return_value=0) #Need to learn more.

        self.calculator.enter_number(-4)
        self.calculator.enter_number(-2)
        self.calculator.multiply()

        self.multiplier.calc.assert_called_with(-4, -2)

    def test_divider_call(self):
        """
        This is to test calculator.divide method call.
        """
        self.divider.calc = MagicMock(return_value=0)

        self.calculator.enter_number(4)
        self.calculator.enter_number(-2)
        self.calculator.divide()

        self.divider.calc.assert_called_with(4, -2)
