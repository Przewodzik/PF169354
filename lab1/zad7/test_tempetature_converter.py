import unittest

from temperature_converter import TemperatureConverter


class TestTemperatureConverter(unittest.TestCase):

    def setUp(self):
        self.converter = TemperatureConverter()

    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(self.converter.celsius_to_fahrenheit(42),107.6,2)

    def test_celsius_to_fahrenheit_negative(self):
        self.assertAlmostEqual(self.converter.celsius_to_fahrenheit(-42),-43.6,2)

    def test_fahrenheit_to_celsius(self):
        self.assertAlmostEqual(self.converter.fahrenheit_to_celsius(107.6),42,2)

    def test_fahrenheit_to_celsius_negative(self):
        self.assertAlmostEqual(self.converter.fahrenheit_to_celsius(-43.6),-42,2)

    def test_celsius_to_kelvin(self):
        self.assertEqual(self.converter.celsius_to_kelvin(0),273.15)

    def test_celsius_to_kelvin_negative(self):
        self.assertEqual(self.converter.celsius_to_kelvin(-1),272.15)

    def test_kelvin_to_celsius(self):
        self.assertEqual(self.converter.kelvin_to_celsius(273.15),0)

    def test_kelvin_to_celsius_negative(self):

        with self.assertRaises(ValueError):
            self.converter.kelvin_to_celsius(-2)

    if __name__ == '__main__':
        unittest.main()