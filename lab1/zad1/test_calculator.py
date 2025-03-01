import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()

    def test_sum_two_ints(self):
        self.assertEqual(self.calc.add(2, 2), 4)

    def test_sum_two_int_negative(self):
        self.assertEqual(self.calc.add(-2, -2), -4)

    def test_subtract_two_ints(self):
        self.assertEqual(self.calc.subtract(2, 4), -2)

    def test_subtract_two_int_negative(self):
        self.assertEqual(self.calc.subtract(-2, -2), 0)

    def test_multiply_two_ints(self):
        self.assertEqual(self.calc.multiply(2, 2), 4)

    def test_multiply_two_int_negative(self):
        self.assertEqual(self.calc.multiply(-2, -2), 4)

    def test_divide_two_ints(self):
        self.assertEqual(self.calc.divide(2, 2), 1)

    def test_divide_two_int_negative(self):
        self.assertEqual(self.calc.divide(-2, -2), 1)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(4, 0)

    if __name__ == "__main__":
        unittest.main()