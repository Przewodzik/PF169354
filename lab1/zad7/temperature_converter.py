
class TemperatureConverter:

    def celsius_to_fahrenheit(self, c):
        return c * 1.8 + 32

    def fahrenheit_to_celsius(self, f):
        return (f - 32) / 1.8

    def celsius_to_kelvin(self, c):
        return c + 273.15

    def kelvin_to_celsius(self,k):

        if k < 0:
            raise ValueError("k must be greater than or equal to zero")
        return k - 273.15
