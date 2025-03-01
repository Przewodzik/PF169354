import unittest

def fibonacci(number):

    if number == 0:
        return 0

    elif number == 1:
        return 1

    return fibonacci(number-1) + fibonacci(number-2)


class TestFibonacci(unittest.TestCase):

    def test_fibonacci_n_0(self):
        self.assertEqual(fibonacci(0), 0)

    def test_fibonacci_n_1(self):
        self.assertEqual(fibonacci(1), 1)

    def test_fibonacci_n_6(self):
        self.assertEqual(fibonacci(6), 8)

    def test_fibonacci_n_16(self):
        self.assertEqual(fibonacci(16), 987)

    def test_fibonacci_n_24(self):
        self.assertEqual(fibonacci(24), 46368)

    if __name__ == '__main__':
        unittest.main()