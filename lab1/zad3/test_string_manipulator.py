import unittest

from lab1.zad3.string_manipulator import StringManipulator


class TestStringManipulator(unittest.TestCase):

    def setUp(self):
        self.string_manipulator = StringManipulator()

    def test_reverse_string(self):
        self.assertEqual(self.string_manipulator.reverse_string("hello world"), "dlrow olleh")

    def test_reverse_string_empty_string(self):
        self.assertEqual(self.string_manipulator.reverse_string(""), "")

    def test_reverse_string_with_symbols(self):
        self.assertEqual(self.string_manipulator.reverse_string("123!@#"), "#@!321")

    def test_count_words(self):
        self.assertEqual(self.string_manipulator.count_words("hello world"), 2)

    def test_count_words_empty(self):
        self.assertEqual(self.string_manipulator.count_words(""), 0)

    def test_count_words_with_symbols(self):
        self.assertEqual(self.string_manipulator.count_words("hello , world !!"), 2)

    def test_count_words_with_multiple_blank_spaces(self):
        self.assertEqual(self.string_manipulator.count_words("    hello    world"),2)

    if __name__ == "__main__":
        unittest.main()