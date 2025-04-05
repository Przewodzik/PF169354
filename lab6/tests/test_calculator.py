import unittest

from lab6.src.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(3, 5), 8)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(1, 1), 0)
        self.assertEqual(self.calc.subtract(0, 5), -5)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(3, 5), 15)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 5), 0)

    def test_divide(self):
        self.assertEqual(self.calc.divide(6, 3), 2)
        self.assertEqual(self.calc.divide(5, 2), 2.5)
        with self.assertRaises(ValueError):
            self.calc.divide(5, 0)

    def test_power(self):
        self.assertEqual(self.calc.power(2, 5), 32)
        self.assertEqual(self.calc.power(2,0), 1)
        self.assertEqual(self.calc.power(0, 0), 1)
        self.assertEqual(self.calc.power(-2, 3), -8)

    def test_square_root(self):
        self.assertEqual(self.calc.square_root(9), 3)
        self.assertEqual(self.calc.square_root(4), 2)
        self.assertEqual(self.calc.square_root(1), 1)

        with self.assertRaises(ValueError):
            self.calc.square_root(-1)

    def test_factorial(self):
        self.assertEqual(self.calc.factorial(3), 6)
        self.assertEqual(self.calc.factorial(5), 120)
        self.assertEqual(self.calc.factorial(0), 1)
        self.assertEqual(self.calc.factorial(1), 1)

        with self.assertRaises(ValueError):
            self.calc.factorial(-1)